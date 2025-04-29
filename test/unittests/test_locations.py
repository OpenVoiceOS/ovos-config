import os
import shutil
from os.path import expanduser, dirname, join, isfile

from unittest import TestCase, mock


class TestLocations(TestCase):
    def test_get_config_dirs(self):
        from ovos_config.locations import get_xdg_config_dirs
        directories = get_xdg_config_dirs("test")
        self.assertIn(expanduser("~/.config/test"), directories)

    def test_get_data_dirs(self):
        from ovos_config.locations import get_xdg_data_dirs
        directories = get_xdg_data_dirs("test")
        self.assertTrue(all((d.endswith('/test') for d in directories)))

    def test_get_xdg_config_save_path(self):
        from ovos_config.locations import get_xdg_config_save_path
        self.assertEqual(get_xdg_config_save_path("test"),
                         expanduser("~/.config/test"))

    def test_get_xdg_data_save_path(self):
        from ovos_config.locations import get_xdg_data_save_path
        self.assertEqual(get_xdg_data_save_path("test"),
                         expanduser("~/.local/share/test"))

    def test_get_xdg_cache_save_path(self):
        from ovos_config.locations import get_xdg_cache_save_path
        self.assertEqual(get_xdg_cache_save_path("test"),
                         expanduser("~/.cache/test"))

    @mock.patch("ovos_config.meta.get_config_filename")
    @mock.patch("ovos_config.locations.get_xdg_config_save_path")
    def test_find_user_config(self, save_path, config_filename):
        config_filename.return_value = "mycroft.yml"
        save_path.return_value = dirname(__file__)
        from ovos_config.locations import find_user_config
        self.assertEqual(find_user_config(), join(dirname(__file__),
                                                  "mycroft.yml"))

    @mock.patch("ovos_config.meta.get_ovos_config")
    @mock.patch("ovos_config.locations.get_webcache_location")
    @mock.patch("ovos_config.locations.get_xdg_config_save_path")
    def test_get_config_locations(self, config_path, webcache_loc,
                                  ovos_config):
        ovos_config.return_value = {
            "test": True,
            "base_folder": "test",
            "config_filename": "test.yaml",
            "default_config_path": "/test/default.yml"
        }
        config_path.return_value = "config"
        webcache_loc.return_value = "webcache"
        from ovos_config.locations import get_config_locations
        self.assertEqual(get_config_locations(False, False, False,
                                              False, False, False
                                              ), list())
        self.assertEqual(get_config_locations(),
                         ['/test/default.yml', '/usr/share/test/test.yaml',
                          '/etc/test/test.yaml', 'webcache',
                          '~/.test/test.yaml', 'config/test.yaml'])


    @mock.patch("ovos_config.meta.get_config_filename")
    @mock.patch("ovos_config.meta.get_xdg_base")
    @mock.patch("os.path.isfile")
    def test_globals(self, fcheck, xdg_base, config_filename):
        fcheck.return_value = True
        xdg_base.return_value = "test"
        config_filename.return_value = "test.yaml"
        os.environ["OVOS_DISTRIBUTION_CONFIG"] = "mycroft/distribution/config"
        os.environ["MYCROFT_SYSTEM_CONFIG"] = "mycroft/system/config"
        os.environ["MYCROFT_WEB_CACHE"] = "mycroft/web/config"

        # Define an ovos.conf file and path for testing
        os.environ['XDG_CONFIG_HOME'] = join(dirname(__file__), "test_config")
        shutil.copy(join(dirname(__file__), "test_config", "test.yaml"),
                    "/tmp/test.yaml")

        # Ensure all globals are reloaded with our test config
        import importlib
        import ovos_config.models

        importlib.reload(ovos_config.locations)
        importlib.reload(ovos_config.meta)

        # Test all config paths respect environment overrides/configured values
        from ovos_config.locations import DEFAULT_CONFIG, DISTRIBUTION_CONFIG, \
            SYSTEM_CONFIG, ASSISTANT_CONFIG, USER_CONFIG, WEB_CONFIG_CACHE

        self.assertEqual(DISTRIBUTION_CONFIG, "mycroft/distribution/config")
        self.assertEqual(SYSTEM_CONFIG, "mycroft/system/config")
        self.assertEqual(USER_CONFIG, join(dirname(__file__), "test_config",
                                           "test/test.yaml"))
        self.assertEqual(ASSISTANT_CONFIG,  join(dirname(__file__), "test_config",
                                           "test/runtime.conf"))
        self.assertEqual(WEB_CONFIG_CACHE, "mycroft/web/config")


        # test default config override
        self.assertTrue(DEFAULT_CONFIG != "/tmp/test.yaml")
        os.environ["OVOS_DEFAULT_CONFIG"] = "/tmp/test.yaml"
        importlib.reload(ovos_config.locations)
        importlib.reload(ovos_config.models)
        importlib.reload(ovos_config.config)
        # Ensure default path is read from env var
        from ovos_config.locations import DEFAULT_CONFIG
        self.assertEqual(DEFAULT_CONFIG, "/tmp/test.yaml")
        # Ensure default config values are present in Configuration object
        from ovos_config.config import Configuration
        self.assertEqual(Configuration.default.path, DEFAULT_CONFIG)
        self.assertTrue(Configuration()["test_config"])
