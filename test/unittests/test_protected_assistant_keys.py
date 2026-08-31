"""protected_keys.assistant lets admins lock individual settings against
writes/reads coming from the assistant layer (runtime.conf), separate from
protected_keys.user / disable_user_config which never touch it.

NOTE: imports are function-level -- see test_merge_cache.py's note on why
(test_locations.py reloads ovos_config.config mid-suite).
"""
import json
import os
import shutil
import tempfile
import unittest
from os.path import join
from unittest.mock import patch


def _config_cls():
    from ovos_config.config import Configuration
    return Configuration


class TestProtectedAssistantKeys(unittest.TestCase):
    def setUp(self):
        Configuration = _config_cls()
        self.tmpdir = tempfile.mkdtemp()
        self.runtime_conf = join(self.tmpdir, "runtime.conf")
        with open(self.runtime_conf, "w") as f:
            json.dump({"secret": "s3cr3t", "lang": "en-us"}, f)

        from ovos_config.models import AssistantConfig
        self._orig_assistant = Configuration.assistant
        # other layers (eg. xdg_configs) are process-wide singletons that may
        # point at this machine's real config; swap them out too so the
        # merge only ever sees this test's own fixtures
        self._orig_xdg_configs = Configuration.xdg_configs
        Configuration.xdg_configs = []
        # keep these patched for the whole test: update_assistant_config()
        # constructs a fresh AssistantConfig() at call time, which reads
        # these same module globals
        self._patches = [
            patch("ovos_config.models.ASSISTANT_CONFIG", self.runtime_conf),
            patch("ovos_config.models.WEB_CONFIG_CACHE",
                 join(self.tmpdir, "nonexistent_web_cache.json")),
        ]
        for p in self._patches:
            p.start()
        Configuration.assistant = AssistantConfig()
        Configuration._invalidate_cache()

    def tearDown(self):
        Configuration = _config_cls()
        for p in self._patches:
            p.stop()
        Configuration.assistant = self._orig_assistant
        Configuration.xdg_configs = self._orig_xdg_configs
        Configuration.reset()
        Configuration._invalidate_cache()
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _with_protection(self, protected):
        Configuration = _config_cls()
        return patch.object(
            Configuration, "get_system_constraints",
            return_value={"protected_keys": {"assistant": protected}})

    def test_protected_key_hidden_from_merge_but_kept_on_disk(self):
        Configuration = _config_cls()
        with self._with_protection(["secret"]):
            Configuration._invalidate_cache()
            merged = Configuration.load_all_configs()
            self.assertNotIn("secret", merged)
            self.assertEqual(merged.get("lang"), "en-us")

            from ovos_config.config import update_assistant_config
            update_assistant_config({"lang": "pt-pt"})

            Configuration._invalidate_cache()
            merged = Configuration.load_all_configs()
            self.assertNotIn("secret", merged,
                             "protected key must stay hidden from the merge")
            self.assertEqual(merged.get("lang"), "pt-pt")

        with open(self.runtime_conf) as f:
            on_disk = json.load(f)
        self.assertEqual(on_disk.get("secret"), "s3cr3t",
                         "protected key must survive on disk, unmodified")
        self.assertEqual(on_disk.get("lang"), "pt-pt")

    def test_update_assistant_config_strips_protected_keys(self):
        from ovos_config.config import update_assistant_config
        with self._with_protection(["secret"]), \
                patch("ovos_config.config.LOG") as mock_log:
            update_assistant_config({"secret": "leaked", "lang": "pt-pt"})
            mock_log.warning.assert_called_once()
            self.assertIn("secret", mock_log.warning.call_args[0][0])

        with open(self.runtime_conf) as f:
            on_disk = json.load(f)
        self.assertEqual(on_disk.get("secret"), "s3cr3t",
                         "assistant must not be able to overwrite a protected key")
        self.assertEqual(on_disk.get("lang"), "pt-pt")

    def test_user_protection_no_longer_applies_to_assistant_layer(self):
        Configuration = _config_cls()
        with patch.object(Configuration, "get_system_constraints",
                          return_value={"protected_keys": {"user": ["secret"]},
                                       "disable_user_config": False}):
            Configuration._invalidate_cache()
            merged = Configuration.load_all_configs()
            self.assertEqual(merged.get("secret"), "s3cr3t",
                             "protected_keys.user must not touch the assistant layer")
