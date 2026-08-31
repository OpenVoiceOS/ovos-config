import json
import os
import shutil
import tempfile
from os.path import join, isfile
from unittest import TestCase, mock


class TestWebcacheMigration(TestCase):
    """Regression tests for the one-time migration of the deprecated
    remote config cache (web_cache.json) into the assistant config layer
    (runtime.conf), see AssistantConfig._migrate_webcache."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.runtime_conf = join(self.tmpdir, "runtime.conf")
        self.web_cache = join(self.tmpdir, "web_cache.json")

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _make_assistant_config(self):
        # patch the module-level path constants AssistantConfig reads
        with mock.patch("ovos_config.models.ASSISTANT_CONFIG", self.runtime_conf), \
                mock.patch("ovos_config.models.WEB_CONFIG_CACHE", self.web_cache):
            from ovos_config.models import AssistantConfig
            return AssistantConfig()

    def test_populated_webcache_is_merged_into_empty_runtime_conf(self):
        with open(self.web_cache, "w") as f:
            json.dump({"location": {"city": {"name": "Lisbon"}}}, f)
        with open(self.runtime_conf, "w") as f:
            json.dump({}, f)

        conf = self._make_assistant_config()

        self.assertEqual(conf["location"]["city"]["name"], "Lisbon")
        with open(self.runtime_conf) as f:
            on_disk = json.load(f)
        self.assertEqual(on_disk["location"]["city"]["name"], "Lisbon")
        # cache file was renamed away, migration is one-time
        self.assertFalse(isfile(self.web_cache))
        self.assertTrue(isfile(self.web_cache + ".migrated"))

    def test_existing_runtime_conf_value_wins(self):
        with open(self.web_cache, "w") as f:
            json.dump({"lang": "en-us"}, f)
        with open(self.runtime_conf, "w") as f:
            json.dump({"lang": "pt-pt"}, f)

        conf = self._make_assistant_config()

        self.assertEqual(conf["lang"], "pt-pt")
        with open(self.runtime_conf) as f:
            on_disk = json.load(f)
        self.assertEqual(on_disk["lang"], "pt-pt")

    def test_missing_webcache_is_a_noop(self):
        with open(self.runtime_conf, "w") as f:
            json.dump({"lang": "en-us"}, f)

        conf = self._make_assistant_config()

        self.assertEqual(conf["lang"], "en-us")
        self.assertFalse(isfile(self.web_cache))
        self.assertFalse(isfile(self.web_cache + ".migrated"))

    def test_migration_runs_once(self):
        with open(self.web_cache, "w") as f:
            json.dump({"location": {"city": {"name": "Lisbon"}}}, f)
        with open(self.runtime_conf, "w") as f:
            json.dump({}, f)

        self._make_assistant_config()
        self.assertTrue(isfile(self.web_cache + ".migrated"))
        self.assertFalse(isfile(self.web_cache))

        # a second load must not touch the already-migrated cache file
        conf2 = self._make_assistant_config()
        self.assertEqual(conf2["location"]["city"]["name"], "Lisbon")
        self.assertTrue(isfile(self.web_cache + ".migrated"))

    def test_corrupt_webcache_does_not_crash_and_skips_migration(self):
        with open(self.web_cache, "w") as f:
            f.write('{"location": {truncated')
        with open(self.runtime_conf, "w") as f:
            json.dump({"lang": "en-us"}, f)

        with mock.patch("ovos_config.models.LOG") as mock_log:
            conf = self._make_assistant_config()

        self.assertEqual(conf["lang"], "en-us")
        # corrupt file is left in place untouched, not renamed away,
        # so a later repair can still migrate it
        self.assertTrue(isfile(self.web_cache))
        self.assertFalse(isfile(self.web_cache + ".migrated"))
        self.assertTrue(mock_log.warning.called)
        self.assertIn("skipping migration", mock_log.warning.call_args[0][0])
