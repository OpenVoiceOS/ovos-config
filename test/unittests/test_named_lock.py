"""The configuration lock holds across processes and threads without combo-lock."""
import os
import re
import subprocess
import sys
import threading
import time
import unittest
from importlib.metadata import requires
from pathlib import Path
from tempfile import gettempdir

HOLD_SECONDS = 1.5

# The holder runs with combo_lock made unimportable, so it proves the package
# works when combo-lock is not installed.
HOLDER = f"""
import sys, time
sys.modules["combo_lock"] = None
from ovos_config.models import LocalConf
with LocalConf._LocalConf__lock:
    print("held", flush=True)
    time.sleep({HOLD_SECONDS})
"""


def requirement_names(dist: str) -> set:
    return {re.split(r"[\s;<>=!~\[]", req, maxsplit=1)[0].lower().replace("_", "-")
            for req in requires(dist) or []}


class TestConfigLock(unittest.TestCase):
    def test_metadata_requires_filelock_not_combo_lock(self):
        names = requirement_names("ovos-config")
        self.assertNotIn("combo-lock", names)
        self.assertIn("filelock", names)

    def test_other_process_waits_for_release(self):
        holder = subprocess.Popen([sys.executable, "-c", HOLDER],
                                  stdout=subprocess.PIPE, text=True)
        try:
            # The package logs to stdout, so skip lines until the marker.
            self.assertIn("held", (line.strip() for line in holder.stdout))
            from ovos_config.models import LocalConf
            start = time.monotonic()
            with LocalConf._LocalConf__lock:
                waited = time.monotonic() - start
        finally:
            holder.wait(timeout=30)
        self.assertEqual(holder.returncode, 0)
        self.assertGreater(waited, HOLD_SECONDS / 2)

    def test_store_in_other_thread_waits_for_release(self):
        from ovos_config.models import LocalConf
        held = threading.Event()

        def hold():
            with LocalConf._LocalConf__lock:
                held.set()
                time.sleep(HOLD_SECONDS)

        holder = threading.Thread(target=hold)
        holder.start()
        self.assertTrue(held.wait(timeout=10))
        conf = LocalConf(None)
        conf["key"] = "value"
        path = Path(gettempdir(), f"ovos_config_lock_test_{os.getpid()}.json")
        try:
            start = time.monotonic()
            conf.store(str(path))
            waited = time.monotonic() - start
        finally:
            holder.join()
            path.unlink(missing_ok=True)
        self.assertGreater(waited, HOLD_SECONDS / 2)

    def test_lock_file_is_the_combo_lock_path(self):
        from ovos_config.models import LocalConf
        lock = LocalConf._LocalConf__lock
        # File name that combo-lock 0.3.1 NamedLock("ovos_config") uses.
        expected = Path(gettempdir(), "combo_locks", "b3Zvc19jb25maWc=.lock")
        self.assertEqual(Path(lock.lock_file), expected)
        with lock:
            self.assertEqual(os.stat(expected).st_mode & 0o777, 0o666)


if __name__ == "__main__":
    unittest.main()
