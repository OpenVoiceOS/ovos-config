import os
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
                                              False, False), list())
        self.assertEqual(get_config_locations(),
                         ['/test/default.yml', '/etc/test/test.yaml',
                          'webcache', '~/.test/test.yaml', 'config/test.yaml'])

    @mock.patch("ovos_config.locations.search_mycroft_core_location")
    def test_find_default_config(self, get_core):
        from ovos_config.locations import find_default_config

        # No Core
        get_core.return_value = None
        no_core_default = find_default_config()
        self.assertTrue(no_core_default.endswith("/ovos_config/mycroft.conf"),
                        no_core_default)
        self.assertTrue(isfile(no_core_default), no_core_default)

        # # Invalid Core
        # get_core.return_value = "/tmp"
        # self.assertEqual(find_default_config(),
        #                  "/tmp/mycroft/configuration/mycroft.conf")

        # Valid Core
        get_core.return_value = dirname(__file__)
        self.assertEqual(find_default_config(),
                         join(dirname(__file__), "mycroft", "configuration",
                              "mycroft.conf"))

    @mock.patch("ovos_utils.system.search_mycroft_core_location")
    @mock.patch("ovos_config.meta.get_config_filename")
    @mock.patch("ovos_config.meta.get_xdg_base")
    def test_globals(self, xdg_base, config_filename, core_location):
        core_location.return_value = "default/config/path"
        xdg_base.return_value = "test"
        config_filename.return_value = "test.yaml"
        os.environ["MYCROFT_SYSTEM_CONFIG"] = "mycroft/system/config"
        os.environ["MYCROFT_WEB_CACHE"] = "mycroft/web/config"
        import importlib
        import ovos_config
        importlib.reload(ovos_config.locations)
        from ovos_config.locations import DEFAULT_CONFIG, SYSTEM_CONFIG, \
            OLD_USER_CONFIG, USER_CONFIG, REMOTE_CONFIG, WEB_CONFIG_CACHE
        self.assertEqual(DEFAULT_CONFIG, "default/config/path/mycroft/configuration/mycroft.conf")
        self.assertEqual(SYSTEM_CONFIG, "mycroft/system/config")
        self.assertEqual(OLD_USER_CONFIG,
                         expanduser("~/.test/test.yaml"))
        self.assertEqual(USER_CONFIG,
                         expanduser("~/.config/test/test.yaml"))
        self.assertEqual(REMOTE_CONFIG, "mycroft.ai")
        self.assertEqual(WEB_CONFIG_CACHE, "mycroft/web/config")
