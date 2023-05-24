import os
import unittest

from os.path import join, dirname


class TestMeta(unittest.TestCase):
    test_dir = join(dirname(__file__), "test_meta")

    @classmethod
    def setUpClass(cls) -> None:
        os.environ["XDG_CONFIG_HOME"] = cls.test_dir
        os.makedirs(cls.test_dir, exist_ok=True)

    def test_get_ovos_config(self):
        from ovos_config.meta import get_ovos_config
        default = get_ovos_config()
        self.assertEqual(default['base_folder'], "mycroft")
        self.assertEqual(default['config_filename'], "mycroft.conf")

        os.environ['OVOS_CONFIG_BASE_FOLDER'] = 'test'
        default = get_ovos_config()
        self.assertEqual(default['base_folder'], "test")
        self.assertEqual(default['config_filename'], "mycroft.conf")

        os.environ['OVOS_CONFIG_FILENAME'] = 'test.yaml'
        default = get_ovos_config()
        self.assertEqual(default['base_folder'], "test")
        self.assertEqual(default['config_filename'], "test.yaml")

        # TODO: Test module_overrides

    def test_save_ovos_config(self):
        from ovos_config.meta import save_ovos_config
        # TODO

    def test_get_ovos_default_config_paths(self):
        from ovos_config.meta import get_ovos_default_config_paths
        # TODO

    def test_get_xdg_base(self):
        from ovos_config.meta import get_xdg_base
        # TODO

    def test_set_xdg_base(self):
        from ovos_config.meta import set_xdg_base
        # TODO

    def test_set_config_filename(self):
        from ovos_config.meta import set_config_filename
        # TODO

    def test_get_config_filename(self):
        from ovos_config.meta import get_config_filename
        # TODO

    def test_set_default_config(self):
        from ovos_config.meta import set_default_config
        # TODO
