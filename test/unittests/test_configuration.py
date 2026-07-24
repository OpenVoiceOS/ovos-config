import importlib
import logging
import shutil
import time

import yaml
import os
import json

from unittest.mock import patch, Mock
from unittest import TestCase
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
        Configuration.load_config_stack([{}])
        # Give file watcher time to initialize
        time.sleep(0.1)
        Configuration._callbacks = []
        # Some tests (eg. test_config_patches_filewatch,
        # test_on_file_change) start a FileWatcher/Observer that is never
        # otherwise stopped. Because ``importlib.reload(ovos_config.config)``
        # re-executes the module in place, any leaked watcher's
        # ``_on_file_change`` staticmethod resolves the module-global name
        # ``Configuration`` at call time -- meaning a stale watcher from a
        # previous test ends up dispatching against the *current* (possibly
        # reloaded) ``Configuration`` state, double-firing callbacks
        # registered by later tests. Shut the watchdog down and clear it so
        # it can't outlive this test.
        if Configuration._watchdog:
            Configuration._watchdog.shutdown()
            Configuration._watchdog = None

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
        user_config = LocalConf(join(test_dir, "user.yaml"))
        Configuration.default = default_config
        Configuration.system = system_config
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
                                                  "from_rem": False,
                                                  "from_usr": True})
        # Test nested constraints
        self.assertEqual(config["test"], {"default": True,
                                          "system": True,
                                          "user": True,
                                          "remote": False})
        # Test non-overridden default config
        self.assertEqual(config["default_only"], "default")
        # Test protected key is undefined
        self.assertFalse("user_only" in config)

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
        thread_config: dict = {}

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
        test_file = join(self.test_dir, "mycroft", "mycroft.conf")
        with open(test_file, 'w+') as f:
            f.write('{"testing": true}')

        import ovos_config
        importlib.reload(ovos_config.config)
        from ovos_config.config import Configuration
        config = Configuration()
        test_cfg = [c for c in config.xdg_configs if c.path == test_file][0]
        self.assertTrue(config['testing'])
        self.assertEqual(dict(test_cfg), {'testing': True})
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
        self.assertEqual(dict(test_cfg), {'testing': True})
        callback.assert_not_called()

        # Test file changed
        with open(test_file, 'w') as f:
            json.dump({"testing": False}, f)
        self.assertTrue(called.wait(2))
        self.assertEqual(dict(test_cfg), {'testing': False})
        callback.assert_called_once()
        self.assertFalse(config['testing'])

    def test_config_created_after_boot_is_watched(self):
        """A config file that does not exist yet must still be watched.

        A device that has never been configured has no user config. If the
        watcher only ever looks at files that already exist, the very first
        write to it is invisible and every running service keeps the old
        values until it restarts -- which is the one write a new device is
        guaranteed to make.
        """
        test_file = join(self.test_dir, "mycroft", "mycroft.conf")
        if isfile(test_file):
            os.remove(test_file)  # a device that has never been configured

        import ovos_config
        importlib.reload(ovos_config.config)
        from ovos_config.config import Configuration
        config = Configuration()
        self.assertIn(test_file, [c.path for c in config.xdg_configs])

        called = Event()
        callback = Mock(side_effect=lambda: called.set())
        config.set_config_watcher(callback)

        with open(test_file, 'w') as f:
            json.dump({"testing": True}, f)

        self.assertTrue(called.wait(5),
                        "creating the config did not reach the watcher")
        self.assertTrue(config['testing'])

    def test_on_file_changes_not_called(self):
        import ovos_config
        importlib.reload(ovos_config.config)

        done = Event()
        threads = []
        call_count = 0

        changed = Event()
        on_file_change = Mock(side_effect=lambda x: changed.set())
        ovos_config.config.Configuration._on_file_change = on_file_change
        ovos_config.config.Configuration.set_config_watcher(Mock())

        test_file = join(self.test_dir, "mycroft", "mycroft.conf")
        with open(test_file, 'w+') as f:
            f.write('{"testing": true}')

        # Test file read
        def _modify_test_file():
            with open(test_file, "r"):
                pass
            nonlocal call_count
            call_count += 1
            if call_count >= len(threads):
                done.set()

        self.assertTrue(changed.wait(2))
        on_file_change.assert_called_once()
        on_file_change.reset_mock()
        for i in range(16):
            thread = Thread(target=_modify_test_file, daemon=True)
            threads.append(thread)

        [thread.start() for thread in threads]
        [thread.join() for thread in threads]
        self.assertTrue(done.wait(30), call_count)
        on_file_change.assert_not_called()

    def test_set_config_watcher(self):
        from ovos_config.config import Configuration
        callback = Mock()
        config = Configuration()
        config.set_config_watcher(callback)
        self.assertEqual(len(config._callbacks), 1)
        config.set_config_watcher(callback)
        self.assertEqual(len(config._callbacks), 1)


class TestMycroftConfigUpdateRegression(TestCase):
    """
    Regression tests for the update_mycroft_config / update_assistant_config
    layering bug: update_mycroft_config must keep writing to USER_CONFIG (or
    an explicit path), NEVER to the assistant/runtime layer, since USER
    outranks ASSISTANT in the merge order and a silent redirect makes every
    existing caller a no-op whenever the key is already set by the user.
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls._orig_environ = dict(os.environ)
        cls.tmp_dir = join(dirname(__file__), "test_config", "mycroft_update_regression")
        os.makedirs(cls.tmp_dir, exist_ok=True)
        for var in ("XDG_CONFIG_HOME", "XDG_DATA_HOME", "XDG_STATE_HOME", "XDG_CACHE_HOME"):
            os.environ[var] = cls.tmp_dir
        import ovos_config
        import ovos_config.locations
        import ovos_config.models
        import ovos_config.config
        importlib.reload(ovos_config.locations)
        importlib.reload(ovos_config.models)
        importlib.reload(ovos_config.config)

    @classmethod
    def tearDownClass(cls) -> None:
        os.environ.clear()
        os.environ.update(cls._orig_environ)
        shutil.rmtree(cls.tmp_dir, ignore_errors=True)
        import ovos_config
        import ovos_config.locations
        import ovos_config.models
        import ovos_config.config
        importlib.reload(ovos_config.locations)
        importlib.reload(ovos_config.models)
        importlib.reload(ovos_config.config)

    def test_update_mycroft_config_writes_user_not_runtime(self):
        from ovos_config.config import Configuration, update_mycroft_config
        from ovos_config.locations import USER_CONFIG, ASSISTANT_CONFIG

        # tests in this class run in alphabetical order (unittest/pytest
        # default), so runtime.conf may already exist from another test;
        # what matters is that THIS call does not add/modify a "lang" key
        # in the assistant layer
        runtime_before = {}
        if isfile(ASSISTANT_CONFIG):
            with open(ASSISTANT_CONFIG) as f:
                runtime_before = json.load(f) or {}
        self.assertNotIn("lang", runtime_before)

        with self.assertWarns(DeprecationWarning):
            update_mycroft_config({"lang": "de-de"})

        self.assertTrue(isfile(USER_CONFIG))
        if isfile(ASSISTANT_CONFIG):
            with open(ASSISTANT_CONFIG) as f:
                runtime_after = json.load(f) or {}
            self.assertNotIn("lang", runtime_after,
                             "update_mycroft_config must not write to runtime.conf")

        with open(USER_CONFIG) as f:
            self.assertEqual(json.load(f).get("lang"), "de-de")

        # merged Configuration() must reflect the change once the (in-memory)
        # user config layer is reloaded from disk -- this is what the real
        # FileWatcher does when USER_CONFIG changes on disk
        Configuration.reload()
        self.assertEqual(Configuration()["lang"], "de-de")

    def test_update_mycroft_config_with_explicit_path(self):
        from ovos_config.config import update_mycroft_config
        from ovos_config.locations import USER_CONFIG

        explicit_path = join(self.tmp_dir, "explicit.conf")
        with self.assertWarns(DeprecationWarning):
            conf = update_mycroft_config({"foo": "bar"}, path=explicit_path)

        self.assertEqual(conf.path, explicit_path)
        self.assertTrue(isfile(explicit_path))
        with open(explicit_path) as f:
            self.assertEqual(json.load(f).get("foo"), "bar")
        # must not have touched the user config for this call
        if isfile(USER_CONFIG):
            with open(USER_CONFIG) as f:
                self.assertNotIn("foo", json.load(f))

    def test_update_assistant_config_writes_runtime_not_user(self):
        from ovos_config.config import Configuration, update_assistant_config
        from ovos_config.locations import USER_CONFIG, ASSISTANT_CONFIG

        update_assistant_config({"secondary_lang": "pt-pt"})

        self.assertTrue(isfile(ASSISTANT_CONFIG))
        with open(ASSISTANT_CONFIG) as f:
            self.assertEqual(json.load(f).get("secondary_lang"), "pt-pt")
        if isfile(USER_CONFIG):
            with open(USER_CONFIG) as f:
                self.assertNotIn("secondary_lang", json.load(f))

        # in-process read must reflect the change immediately, without
        # needing a bus patch or the file watcher to intervene
        self.assertEqual(Configuration.assistant.get("secondary_lang"), "pt-pt")
        self.assertEqual(Configuration()["secondary_lang"], "pt-pt")

    def test_get_config_locations_includes_assistant(self):
        from ovos_config.locations import get_config_locations, ASSISTANT_CONFIG
        locs = get_config_locations()
        self.assertIn(ASSISTANT_CONFIG, locs)


class TestPR194BackwardsCompat(TestCase):
    """
    Regression tests for the four API removals restored in PR #194
    (feat/assistant_config): a breaking change must ship in two releases,
    the first of which keeps every existing API working (with a
    DeprecationWarning) and only a later `chore!: remove deprecated code`
    release may delete anything. These tests pin the five call shapes that
    must keep working so a future removal is caught by CI.
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls._orig_environ = dict(os.environ)
        cls.tmp_dir = join(dirname(__file__), "test_config", "pr194_backcompat")
        os.makedirs(cls.tmp_dir, exist_ok=True)
        for var in ("XDG_CONFIG_HOME", "XDG_DATA_HOME", "XDG_STATE_HOME", "XDG_CACHE_HOME"):
            os.environ[var] = cls.tmp_dir
        import ovos_config
        import ovos_config.locations
        import ovos_config.models
        import ovos_config.config
        importlib.reload(ovos_config.locations)
        importlib.reload(ovos_config.models)
        importlib.reload(ovos_config.config)

    @classmethod
    def tearDownClass(cls) -> None:
        os.environ.clear()
        os.environ.update(cls._orig_environ)
        shutil.rmtree(cls.tmp_dir, ignore_errors=True)
        import ovos_config
        import ovos_config.locations
        import ovos_config.models
        import ovos_config.config
        importlib.reload(ovos_config.locations)
        importlib.reload(ovos_config.models)
        importlib.reload(ovos_config.config)

    def test_configuration_remote_attribute(self):
        from ovos_config.config import Configuration
        from ovos_config.models import RemoteConf

        with self.assertWarns(DeprecationWarning):
            remote = Configuration.remote
        self.assertIsInstance(remote, RemoteConf)
        # must not be re-added to the merge stack
        merged = Configuration.load_all_configs()
        self.assertIsInstance(merged, dict)

    def test_configuration_remote_attribute_from_instance(self):
        # on dev, `remote` was a plain class attribute, so it was reachable
        # both as Configuration.remote AND Configuration().remote -- a
        # metaclass property alone only restores the class-level form, so
        # this pins the instance-level form too
        from ovos_config.config import Configuration
        from ovos_config.models import RemoteConf

        instance = Configuration()
        remote = instance.remote
        self.assertIsInstance(remote, RemoteConf)
        # both accessors must share the single cached RemoteConf instance,
        # since RemoteConf() warns on every construction and dev only ever
        # had one shared object
        self.assertIs(Configuration.remote, instance.remote)

    def test_handle_remote_update_is_a_deprecated_noop(self):
        from ovos_config.config import Configuration

        with self.assertWarns(DeprecationWarning):
            # must not raise, even though remote config isn't part of the
            # merge stack anymore
            self.assertIsNone(Configuration.handle_remote_update(None))

    def test_load_config_stack_accepts_cache_and_remote_kwargs(self):
        from ovos_config.config import Configuration

        # must not raise TypeError for callers still passing the old kwargs
        result = Configuration.load_config_stack(cache=True, remote=False)
        self.assertIsInstance(result, dict)

        # defaulted (not explicitly passed) call must still work too
        result = Configuration.load_config_stack()
        self.assertIsInstance(result, dict)

    def test_mycroft_system_config_forwards_allow_overwrite(self):
        from ovos_config.models import MycroftSystemConfig

        with self.assertWarns(DeprecationWarning):
            cfg = MycroftSystemConfig(allow_overwrite=True)
        self.assertTrue(cfg.allow_overwrite)

    def test_ovos_distribution_config_forwards_allow_overwrite(self):
        from ovos_config.models import OvosDistributionConfig

        with self.assertWarns(DeprecationWarning):
            cfg = OvosDistributionConfig(allow_overwrite=True)
        self.assertTrue(cfg.allow_overwrite)
