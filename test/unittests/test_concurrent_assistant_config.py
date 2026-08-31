import json
import os
import shutil
import subprocess
import sys
import tempfile
import textwrap
from os.path import join
from unittest import TestCase

# "process A": a short-lived process that writes a key to runtime.conf,
# independently of the long-lived "process B" driven by _run_long_lived_b().
_WRITE_KEY_SCRIPT = """
import sys, warnings
warnings.simplefilter("ignore")
from ovos_config.config import update_assistant_config
update_assistant_config({sys.argv[1]: sys.argv[2]})
"""

# "process A" variant that rewrites runtime.conf directly, dropping any key
# not passed on the command line (simulates another process deleting a key).
_OVERWRITE_FILE_SCRIPT = """
import json, sys
with open(sys.argv[1], "w") as f:
    json.dump({sys.argv[2]: sys.argv[3]}, f)
"""


class TestConcurrentAssistantConfig(TestCase):
    """update_assistant_config must not clobber runtime.conf writes made by
    other processes between when a long-lived process loaded its config and
    when it later calls update_assistant_config itself."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        os.makedirs(join(self.tmpdir, "mycroft"), exist_ok=True)
        self.runtime_conf = join(self.tmpdir, "mycroft", "runtime.conf")
        with open(join(self.tmpdir, "mycroft", "mycroft.conf"), "w") as f:
            json.dump({}, f)
        self.env = dict(os.environ)
        self.env["XDG_CONFIG_HOME"] = self.tmpdir

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _run(self, script, *args):
        subprocess.run([sys.executable, "-c", script, *args],
                       check=True, env=self.env)

    def _run_long_lived_b(self, extra_body):
        """Runs, in ONE interpreter (mimicking a long-lived process): load
        Configuration, then run `extra_body` (typically: spawn process A,
        then call update_assistant_config) before exiting."""
        script = textwrap.dedent("""
            import warnings, subprocess, sys, os
            warnings.simplefilter("ignore")
            from ovos_config.config import Configuration, update_assistant_config
            Configuration()  # long-lived process loads config once, at start
        """) + extra_body
        self._run(script)

    def test_writes_from_two_processes_both_survive(self):
        with open(self.runtime_conf, "w") as f:
            json.dump({}, f)

        self._run_long_lived_b(textwrap.dedent(f"""
            subprocess.run([sys.executable, "-c", {_WRITE_KEY_SCRIPT!r},
                            "tts", "A"], check=True, env=os.environ)
            update_assistant_config({{"lang": "B"}})
        """))

        with open(self.runtime_conf) as f:
            on_disk = json.load(f)
        self.assertEqual(on_disk.get("tts"), "A")
        self.assertEqual(on_disk.get("lang"), "B")

    def test_deleted_key_does_not_resurrect(self):
        with open(self.runtime_conf, "w") as f:
            json.dump({"tts": "A", "lang": "en-us"}, f)

        self._run_long_lived_b(textwrap.dedent(f"""
            # process A rewrites runtime.conf, dropping "lang" entirely
            subprocess.run([sys.executable, "-c", {_OVERWRITE_FILE_SCRIPT!r},
                            {self.runtime_conf!r}, "tts", "A"],
                           check=True, env=os.environ)
            update_assistant_config({{"extra": "value"}})
        """))

        with open(self.runtime_conf) as f:
            on_disk = json.load(f)
        self.assertNotIn("lang", on_disk)
        self.assertEqual(on_disk.get("tts"), "A")
        self.assertEqual(on_disk.get("extra"), "value")
