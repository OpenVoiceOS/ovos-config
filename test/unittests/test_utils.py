import os
import shutil
import json
import importlib
from copy import deepcopy
from os.path import dirname, join, isfile

from unittest import TestCase


_DEFAULT_CONFIG_PATH = join(dirname(__file__), "mycroft.conf")
_TEST_CONFIG_OVERRIDE = {"base_folder": "neon",
                         "config_filename": "neon.yaml",
                         "default_config_path": _DEFAULT_CONFIG_PATH}


class TestUtils(TestCase):
    def test_init_ovos_conf(self):
        test_config_dir = join(dirname(__file__), "test_init_config")
        from ovos_config.utils import init_module_config
        os.environ["XDG_CONFIG_HOME"] = test_config_dir

        if isfile(join(test_config_dir, "OpenVoiceOS", "ovos.conf")):
            os.remove(join(test_config_dir, "OpenVoiceOS", "ovos.conf"))

        # Init 'test_module' to use 'neon_core' config
        init_module_config("test_module", "neon", _TEST_CONFIG_OVERRIDE)

        with open(join(test_config_dir, "OpenVoiceOS", "ovos.conf")) as f:
            config = json.load(f)

        # Patch local tests

        self.assertEqual(config, {"module_overrides": {
            "neon": {
                "base_folder": "neon",
                "config_filename": "neon.yaml",
                "default_config_path": _DEFAULT_CONFIG_PATH
            }
        },
            "submodule_mappings": {
                "test_module": "neon"
            }})

        # init same module again, config should be unchanged
        init_module_config("test_module", "neon", _TEST_CONFIG_OVERRIDE)
        with open(join(test_config_dir, "OpenVoiceOS", "ovos.conf")) as f:
            config2 = json.load(f)
        # Patch local tests
        config2['module_overrides']['neon'].setdefault(
            'default_config_path', "")
        self.assertEqual(config, config2)

        # init another different module
        init_module_config("other_test_module", "neon", _TEST_CONFIG_OVERRIDE)
        with open(join(test_config_dir, "OpenVoiceOS", "ovos.conf")) as f:
            config3 = json.load(f)

        self.assertEqual(config3, {"module_overrides": {
            "neon": {
                "base_folder": "neon",
                "config_filename": "neon.yaml",
                "default_config_path": _DEFAULT_CONFIG_PATH
            }
        },
            "submodule_mappings": {
                "test_module": "neon",
                "other_test_module": "neon"
            }})

        # init neon_core
        init_module_config("neon_core", "neon", _TEST_CONFIG_OVERRIDE)
        with open(join(test_config_dir, "OpenVoiceOS", "ovos.conf")) as f:
            config4 = json.load(f)
            # Patch local tests
            config4['module_overrides']['neon'].setdefault(
                'default_config_path', "")
        self.assertEqual(config4, {"module_overrides": {
            "neon": {
                "base_folder": "neon",
                "config_filename": "neon.yaml",
                "default_config_path": _DEFAULT_CONFIG_PATH
            }
        },
            "submodule_mappings": {
                "test_module": "neon",
                "other_test_module": "neon",
                "neon_core": "neon"
            }})

        # Override default config with test file
        import inspect
        import ovos_config.models
        import ovos_config.config
        from ovos_config.meta import get_ovos_config

        ovos_config.DEFAULT_CONFIG = join(dirname(__file__), "mycroft"
                                          "configuration", "mycroft.conf")
        old_value = deepcopy(ovos_config.DEFAULT_CONFIG)

        # Init config and validate other config file is loaded
        stack = inspect.stack()
        mod = inspect.getmodule(stack[1][0])
        this_modname = mod.__name__.split('.')[0]
        init_module_config(this_modname, "neon", _TEST_CONFIG_OVERRIDE)
        self.assertNotEqual(old_value, ovos_config.DEFAULT_CONFIG)
        self.assertEqual(ovos_config.models.DEFAULT_CONFIG,
                         ovos_config.DEFAULT_CONFIG)
        self.assertEqual(ovos_config.config.Configuration.default.path,
                         ovos_config.DEFAULT_CONFIG)

        # Test default config
        self.assertTrue(ovos_config.config.Configuration()['default_config'])
        self.assertEqual(get_ovos_config()['default_config_path'],
                         _DEFAULT_CONFIG_PATH)

        # Test module imports
        self.assertEqual(ovos_config.Configuration,
                         ovos_config.config.Configuration)

        # Cleanup configuration and force reload of pre-test defaults
        os.environ.pop("XDG_CONFIG_HOME")
        shutil.rmtree(test_config_dir)
        del ovos_config.config.Configuration
        importlib.reload(ovos_config.locations)
        importlib.reload(ovos_config.models)
        importlib.reload(ovos_config.config)
