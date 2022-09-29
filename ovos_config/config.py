# Copyright 2017 Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import json
from os.path import isfile
from time import sleep

from mycroft_bus_client import Message

from ovos_config.models import LocalConf, MycroftDefaultConfig, MycroftSystemConfig, MycroftUserConfig, RemoteConf
from ovos_config.locations import OLD_USER_CONFIG, get_xdg_config_save_path, get_xdg_config_locations
from ovos_config.utils import FileWatcher

from ovos_utils.json_helper import flattened_delete, merge_dict
from ovos_utils.log import LOG
from ovos_utils.network_utils import is_connected


def _log_old_location_deprecation(old_user_config=OLD_USER_CONFIG):
    LOG.warning(" ===============================================")
    LOG.warning(" ==             DEPRECATION WARNING           ==")
    LOG.warning(" ===============================================")
    LOG.warning(f" You still have a config file at {old_user_config}")
    LOG.warning(" Note that this location is deprecated and will" +
                " not be used in the future")
    LOG.warning(" Please move it to " + get_xdg_config_save_path())


class Configuration(dict):
    """Namespace for operations on the configuration singleton."""
    __patch = LocalConf(None)  # Patch config that skills can update to override config
    bus = None
    default = MycroftDefaultConfig()
    system = MycroftSystemConfig()
    remote = RemoteConf()
    # This includes both the user config and
    # /etc/xdg/mycroft/mycroft.conf
    xdg_configs = [LocalConf(p) for p in get_xdg_config_locations()]
    _old_user = LocalConf(OLD_USER_CONFIG)
    # deprecation warning
    if isfile(OLD_USER_CONFIG):
        _log_old_location_deprecation(OLD_USER_CONFIG)
    _watchdog = None
    _callbacks = []

    def __init__(self):
        # python does not support proper overloading
        # when instantiation a Configuration object (new style)
        # the get method is replaced for proper dict behaviour
        self.get = self._real_get
        super().__init__(**self.load_all_configs())

    # dict methods
    def __setitem__(self, key, value):
        Configuration.__patch[key] = value
        super().__setitem__(key, value)
        # sync with other processes connected to bus
        if Configuration.bus:
            Configuration.bus.emit(Message("configuration.patch",
                                           {"config": {key: value}}))

    def __getitem__(self, item):
        super().update(Configuration.load_all_configs())
        return super().get(item)

    def __str__(self):
        super().update(Configuration.load_all_configs())
        try:
            return json.dumps(self, sort_keys=True)
        except:
            return super().__str__()

    def __dict__(self):
        super().update(Configuration.load_all_configs())
        return self

    def __repr__(self):
        return self.__str__()

    def __iter__(self):
        super().update(Configuration.load_all_configs())
        for k in super().__iter__():
            yield k

    def update(self, *args, **kwargs):
        Configuration.__patch.update(*args, **kwargs)
        super().update(*args, **kwargs)

    def pop(self, key):
        # we can not pop the key because configs are read only
        # we could do it for __patch but that does not make sense
        # for the object as a whole which is
        # supposed to behave like a python dict
        self.__setitem__(key, None)

    def items(self):
        super().update(Configuration.load_all_configs())
        return super().items()

    def keys(self):
        super().update(Configuration.load_all_configs())
        return super().keys()

    def values(self):
        super().update(Configuration.load_all_configs())
        return super().values()

    # config methods
    @staticmethod
    def load_config_stack(configs=None, cache=False, remote=True):
        """Load a stack of config dicts into a single dict

        Args:
            configs (list): list of dicts to load
            cache (boolean): True if result should be cached
            remote (boolean): False if the Mycroft Home settings shouldn't
                              be loaded
        Returns:
            (dict) merged dict of all configuration files
        """
        LOG.warning("load_config_stack has been deprecated, use load_all_configs instead")
        if configs:
            return Configuration.filter_and_merge(configs)
        system_constraints = Configuration.get_system_constraints()
        if not remote:
            system_constraints["disable_remote_config"] = True
        return Configuration.load_all_configs(system_constraints)

    @staticmethod
    def reset():
        Configuration.__patch = {}
        Configuration.reload()

    @staticmethod
    def reload():
        Configuration.default.reload()
        Configuration.system.reload()
        Configuration.remote.reload()
        for cfg in Configuration.xdg_configs:
            cfg.reload()

    @staticmethod
    def get_system_constraints():
        # constraints must come from SYSTEM config
        # if not defined then load the DEFAULT constraints
        # these settings can not be set anywhere else!
        return Configuration.system.get("system") or \
               Configuration.default.get("system") or \
               {}

    @staticmethod
    def load_all_configs(system_constraints=None):
        """Load the stack of config files into a single dict

        Returns:
            (dict) merged dict of all configuration files
        """
        # system administrators can define different constraints in how
        # configurations are loaded
        system_constraints = system_constraints or Configuration.get_system_constraints()
        skip_user = system_constraints.get("disable_user_config", False)
        skip_remote = system_constraints.get("disable_remote_config", False)

        configs = [Configuration.default, Configuration.system]
        if not skip_remote:
            configs.append(Configuration.remote)
        if not skip_user:
            # deprecation warning
            if isfile(OLD_USER_CONFIG):
                configs.append(Configuration._old_user)
            configs += Configuration.xdg_configs

        # runtime patches by skills / bus events
        configs.append(Configuration.__patch)

        # Merge all configs into one
        return Configuration.filter_and_merge(configs)

    @staticmethod
    def filter_and_merge(configs):
        # ensure type
        for index, item in enumerate(configs):
            if isinstance(item, str):
                configs[index] = LocalConf(item)
            elif not isinstance(item, LocalConf):
                configs[index] = LocalConf(None)
                configs[index].merge(item)

        # system administrators can define different constraints in how
        # configurations are loaded
        system_conf = Configuration.get_system_constraints()
        protected_keys = system_conf.get("protected_keys") or {}
        protected_remote = protected_keys.get("remote") or []
        protected_user = protected_keys.get("user") or []
        skip_user = system_conf.get("disable_user_config", False)
        skip_remote = system_conf.get("disable_remote_config", False)

        # Merge all configs into one
        base = {}
        for cfg in configs:
            is_user = cfg.path is None or cfg.path not in [Configuration.default.path,
                                                           Configuration.system.path]
            is_remote = cfg.path == Configuration.remote.path
            if (is_remote and skip_remote) or (is_user and skip_user):
                continue
            elif is_remote:
                # delete protected keys from remote config
                for protection in protected_remote:
                    flattened_delete(cfg, protection)
            elif is_user:
                # delete protected keys from user config
                for protection in protected_user:
                    flattened_delete(cfg, protection)
            merge_dict(base, cfg)
        return base

    @staticmethod
    def set_config_update_handlers(bus):
        """Setup websocket handlers to update config.

        Args:
            bus: Message bus client instance
        """
        # remove any old event listeners
        Configuration.deregister_bus()

        # attach new bus and listeners
        Configuration.bus = bus
        bus.on("configuration.updated", Configuration.updated)
        bus.on("configuration.patch", Configuration.patch)
        bus.on("configuration.patch.clear", Configuration.patch_clear)
        bus.on("configuration.cache.clear", Configuration.clear_cache)
        # TODO unify these namespaces, they seem to differ between dev/mk2/PHAL
        bus.on("mycroft.paired", Configuration.handle_remote_update)
        bus.on("mycroft.internet.connected", Configuration.handle_remote_update)

        Configuration.set_config_watcher()

        # do the initial remote fetch
        if is_connected():
            Configuration.remote.reload()

    @staticmethod
    def set_config_watcher(callback=None):
        """Setup filewatcher to monitor for config file changes"""
        paths = [Configuration.system.path] + \
                [c.path for c in Configuration.xdg_configs]
        if callback:
            Configuration._callbacks.append(callback)
        if not Configuration._watchdog:
            Configuration._watchdog = FileWatcher(
                [p for p in paths if isfile(p)],
                Configuration._on_file_change
            )

    @staticmethod
    def _on_file_change(path):
        LOG.info(f'{path} changed on disk, reloading!')
        # reload updated config
        for cfg in Configuration.xdg_configs + [Configuration.system]:
            if cfg.path == path:
                try:
                    cfg.reload()
                except:
                    # got the file changed signal before write finished
                    sleep(0.5)
                    try:
                        cfg.reload()
                    except:
                        LOG.exception("Failed to load configuration, syntax seems invalid!")
                break
        else:
            # reload all configs
            try:
                Configuration.reload()
            except:
                # got the file changed signal before write finished
                sleep(0.5)
                try:
                    Configuration.reload()
                except:
                    LOG.exception("Failed to load configuration, syntax seems invalid!")

        for handler in Configuration._callbacks:
            try:
                handler()
            except:
                LOG.exception("Error in config update callback handler")

    @staticmethod
    def deregister_bus():
        if Configuration.bus:
            Configuration.bus.remove("configuration.updated", Configuration.updated)
            Configuration.bus.remove("configuration.patch", Configuration.patch)
            Configuration.bus.remove("configuration.patch.clear", Configuration.patch_clear)
            Configuration.bus.remove("configuration.cache.clear", Configuration.clear_cache)
            Configuration.bus.remove("mycroft.paired", Configuration.handle_remote_update)
            Configuration.bus.remove("mycroft.internet.connected", Configuration.handle_remote_update)

    @staticmethod
    def handle_remote_update(message):
        """Handler for paired/internet connect

        Triggers an update of remote config.
        """
        Configuration.remote.reload()

    @staticmethod
    def updated(message):
        """Handler for configuration.updated,

        Triggers an update of cached config.
        """
        Configuration.reload()

    @staticmethod
    def patch(message):
        """Patch the volatile dict usable by skills

        Args:
            message: Messagebus message should contain a config
                     in the data payload.
        """
        config = message.data.get("config", {})
        for k, v in config.items():
            Configuration.__patch[k] = v

    @staticmethod
    def patch_clear(message):
        """Clear the config patch space.

        Args:
            message: Messagebus message should contain a config
                     in the data payload.
        """
        Configuration.__patch = {}

    # Backwards compat methods
    @staticmethod
    def get(configs=None, cache=True, remote=True):
        """DEPRECATED - use Configuration class instead"""
        LOG.warning("Configuration.get() has been deprecated, use Configuration() instead")
        # NOTE: this is only called if using the class directly
        # if using an instance (dict object) self._real_get is called instead
        return Configuration.load_config_stack(configs, cache, remote)

    def _real_get(self, key, default=None):
        return self.__getitem__(key) or default

    @staticmethod
    def clear_cache(message=None):
        """DEPRECATED - there is no cache anymore """
        Configuration.updated(message)


def read_mycroft_config():
    """ returns a stateless dict with the loaded configuration """
    return dict(Configuration())


def update_mycroft_config(config, path=None, bus=None):
    """ updates user config file with the contents of provided dict
    if a path is provided that location will be used instead of MycroftUserConfig"""
    if path is None:
        conf = MycroftUserConfig()
    else:
        conf = LocalConf(path)
    conf.merge(config)
    conf.store()
    if bus:  # inform all Configuration objects connected to the bus
        bus.emit(Message("configuration.patch",  {"config": config}))
    return conf
