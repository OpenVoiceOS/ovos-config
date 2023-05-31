import logging
import shutil
import yaml
import os
import json

from unittest.mock import MagicMock, patch, Mock
from unittest import TestCase, skip
from threading import Event, Thread
from os.path import dirname, isfile, join
from typing import OrderedDict
from ovos_utils.log import LOG

LOG.level = logging.DEBUG


class TestConfiguration(TestCase):
    test_dir = join(dirname(__file__), "test_config", "test")

    @classmethod
    def setUpClass(cls) -> None:
        os.environ['XDG_CONFIG_HOME'] = cls.test_dir
        os.makedirs(join(cls.test_dir, "mycroft"), exist_ok=True)
        with open(join(cls.test_dir, "mycroft", "mycroft.conf"), 'w') as f:
            f.write('{"testing": true}')

        from ovos_config import Configuration

    @classmethod
    def tearDownClass(cls) -> None:
        os.environ.pop('XDG_CONFIG_HOME')
        shutil.rmtree(cls.test_dir)

    def tearDown(self):
        from ovos_config.config import Configuration
        Configuration.load_config_stack([{}], True)

    def test_get(self):
        from ovos_config.config import Configuration
        d1 = {'a': 1, 'b': {'c': 1, 'd': 2}}
        d2 = {'b': {'d': 'changed'}}
        d = Configuration.get([d1, d2])
        self.assertEqual(d['a'], d1['a'])
        self.assertEqual(d['b']['d'], d2['b']['d'])
        self.assertEqual(d['b']['c'], d1['b']['c'])

    @patch('mycroft.api.DeviceApi')
    @skip("requires backend to be enabled, TODO refactor test!")
    def test_remote(self, mock_api):
        from ovos_config.models import RemoteConf
        remote_conf = {'TestConfig': True, 'uuid': 1234}
        remote_location = {'city': {'name': 'Stockholm'}}
        dev_api = MagicMock()
        dev_api.get_settings.return_value = remote_conf
        dev_api.get_location.return_value = remote_location
        mock_api.return_value = dev_api

        rc = RemoteConf()
        self.assertTrue(rc['test_config'])
        self.assertEqual(rc['location']['city']['name'], 'Stockholm')

    @patch('json.dump')
    @patch('ovos_config.models.exists')
    @patch('ovos_config.models.isfile')
    @patch('ovos_config.models.load_commented_json')
    def test_local(self, mock_json_loader, mock_isfile, mock_exists,
                   mock_json_dump):
        from ovos_config.models import LocalConf
        local_conf = {'answer': 42, 'falling_objects': ['flower pot', 'whale']}
        mock_exists.return_value = True
        mock_isfile.return_value = True
        mock_json_loader.return_value = local_conf
        lc = LocalConf('test')
        self.assertEqual(lc, local_conf)

        # Test merge method
        merge_conf = {'falling_objects': None, 'has_towel': True}
        lc.merge(merge_conf)
        self.assertEqual(lc['falling_objects'], None)
        self.assertEqual(lc['has_towel'], True)

        # test store
        lc.store('test_conf.json')
        self.assertEqual(mock_json_dump.call_args[0][0], lc)
        # exists but is not file
        mock_isfile.return_value = False
        lc = LocalConf('test')
        self.assertEqual(lc, {})

        # does not exist
        mock_exists.return_value = False
        lc = LocalConf('test')
        self.assertEqual(lc, {})

    def test_local_config_exceptions(self):
        from ovos_config.models import LocalConf
        missing_path = join(dirname(__file__), "file_not_found.json")
        invalid_path = __file__
        invalid_yaml = join(dirname(__file__), "invalid_yaml.yaml")

        conf = LocalConf(missing_path)
        self.assertEqual(conf, dict())

        conf = LocalConf(invalid_path)
        self.assertEqual(conf, dict())

        conf = LocalConf(invalid_yaml)
        self.assertEqual(conf, dict())

    def test_file_formats(self):
        from ovos_config.models import LocalConf
        yml_cnf = LocalConf(f"{dirname(__file__)}/mycroft.yml")
        json_config = LocalConf(f"{dirname(__file__)}/mycroft.json")
        self.assertEqual(json_config, yml_cnf)

        # test export json config as yaml
        json_config.store("/tmp/not_mycroft.yml")
        self.assertTrue(isfile("/tmp/not_mycroft.yml"))
        test_conf = LocalConf("/tmp/not_mycroft.yml")
        self.assertEqual(test_conf, yml_cnf)
        self.assertEqual(test_conf, json_config)

        # test export yaml config as json
        yml_cnf.store("/tmp/not_mycroft.json")
        self.assertTrue(isfile("/tmp/not_mycroft.json"))
        test_conf = LocalConf("/tmp/not_mycroft.json")
        self.assertEqual(test_conf, yml_cnf)
        self.assertEqual(test_conf, json_config)

        with open("/tmp/not_mycroft.yml") as f:
            disk_yml = yaml.safe_load(f)
        self.assertEqual(yml_cnf, disk_yml)

        with open("/tmp/not_mycroft.json") as f:
            disk_json = json.load(f)
        self.assertEqual(test_conf, disk_json)

        self.assertEqual(disk_yml, disk_json)

    def test_yaml_config_load(self):
        from ovos_config.models import LocalConf
        yml_cnf = LocalConf(f"{dirname(__file__)}/mycroft.yml")
        for d in (yml_cnf, yml_cnf["hotwords"],
                  yml_cnf["hotwords"]["hey mycroft"],
                  yml_cnf["hotwords"]["wake up"]):
            self.assertIsInstance(d, dict)
            self.assertNotIsInstance(d, OrderedDict)
            self.assertEqual(json.loads(json.dumps(d)), d)

    def test_load_config_stack(self):
        from ovos_config.models import LocalConf
        from ovos_config.config import Configuration
        test_dir = join(dirname(__file__), "config_stack")
        default_config = LocalConf(join(test_dir, "default.yaml"))
        system_config = LocalConf(join(test_dir, "system.yaml"))
        remote_config = LocalConf(join(test_dir, "remote.yaml"))
        user_config = LocalConf(join(test_dir, "user.yaml"))
        Configuration.default = default_config
        Configuration.system = system_config
        Configuration.remote = remote_config
        Configuration.xdg_configs = [user_config]
        Configuration.__patch = LocalConf(None)
        Configuration._old_user = LocalConf(None)
        Configuration.load_all_configs()
        config = Configuration()
        # Test stack load order
        self.assertEqual(config["config_name"], "user")
        # Test system constraints
        self.assertEqual(config["system_only"], {"from_sys": True,
                                                 "from_rem": False,
                                                 "from_usr": False})
        # Test default constraints (overridden)
        self.assertEqual(config["default_spec"], {"from_sys": True,
                                                  "from_rem": True,
                                                  "from_usr": True})
        # Test nested constraints
        self.assertEqual(config["test"], {"default": True,
                                          "system": True,
                                          "user": True,
                                          "remote": True})
        # Test non-overridden default config
        self.assertEqual(config["default_only"], "default")
        # Test protected key is undefined
        self.assertFalse("user_only" in config)
        self.assertEqual(config["remote_only"], "remote")

    def test_config_patches_filewatch(self):
        event = Event()
        thread_config = None

        def _wait_for_changes():
            nonlocal thread_config
            from ovos_config.config import Configuration
            thread_config = Configuration()
            thread_config.set_config_watcher(lambda: event.set())
            event.wait()

        thread = Thread(target=_wait_for_changes, daemon=True)
        thread.start()
        from ovos_config.config import Configuration
        config = Configuration()
        while not thread_config:
            event.wait(1)
        self.assertEqual(config, thread_config)
        self.assertEqual(len(thread_config._callbacks), len(config._callbacks))
        self.assertEqual(len(thread_config._callbacks), 1)

        # Update config, thread is unchanged
        config['test_threading'] = 'value'
        self.assertEqual(config['test_threading'], 'value')
        self.assertFalse(event.wait(5))
        self.assertNotEqual(config, thread_config)

        # Write changes to disk, thread is updated
        from ovos_config.config import update_mycroft_config
        updated = update_mycroft_config(config)
        self.assertEqual(updated, config)
        self.assertEqual(config['test_threading'], 'value')
        self.assertTrue(event.wait(10))
        # Config objects are different, but contents should be same
        self.assertEqual(str(config), str(thread_config))

        self.assertIsNone(thread.join(0))

    def test_config_patches_messagebus(self):
        from threading import Event
        from ovos_utils.messagebus import FakeBus
        event = Event()
        bus = FakeBus()
        thread_config = None

        def _wait_for_changes():
            nonlocal thread_config
            from ovos_config.config import Configuration
            thread_config = Configuration()
            thread_config.set_config_update_handlers(bus)
            event.wait()

        patched_callback = Mock(side_effect=event.set())
        bus.once("configuration.patch", patched_callback)

        thread = Thread(target=_wait_for_changes, daemon=True)
        thread.start()
        from ovos_config.config import Configuration
        config = Configuration()
        while not thread_config:
            event.wait(1)
        self.assertEqual(config, thread_config)
        # global bus should be available to both config objects
        self.assertEqual(config.bus, thread_config.bus)
        self.assertEqual(config.bus, bus)

        # Update config, thread should be patched
        config['test_threading'] = 'patched'
        self.assertTrue(event.wait(10))
        patched_callback.assert_called_once()
        patch = patched_callback.call_args[0][0].data['config']
        self.assertEqual(patch, {"test_threading": "patched"})
        # Config objects are different, but contents should be same
        self.assertEqual(str(config), str(thread_config))

        self.assertIsNone(thread.join(0))

    def test_on_file_change(self):
        from ovos_config.config import Configuration
        test_file = join(self.test_dir, "mycroft", "mycroft.conf")

        config = Configuration()
        self.assertTrue(config['testing'])
        called = Event()
        callback = Mock(side_effect=lambda: called.set())
        config.set_config_watcher(callback)
        self.assertIn(test_file, [c.path for c in config.xdg_configs])

        # Test file opened with no changes
        with open(test_file, 'a') as f:
            pass
        self.assertFalse(called.wait(2))
        callback.assert_not_called()

        # Test file opened with no config changes
        with open(test_file, 'a') as f:
            f.write("\n\n// Comment")
        self.assertFalse(called.wait(2))
        callback.assert_not_called()

        # Test file changed
        with open(test_file, 'w') as f:
            json.dump({"testing": False}, f)
        self.assertTrue(called.wait(2))
        callback.assert_called_once()
        self.assertFalse(config['testing'])
