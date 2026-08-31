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
import warnings
from typing import Optional

from ovos_config.locations import get_xdg_config_locations
from ovos_config.models import LocalConf, DefaultConfig, DistributionConfig, SystemConfig, AssistantConfig, \
    UserConfig, MycroftDefaultConfig, OvosDistributionConfig, MycroftSystemConfig, MycroftUserConfig, RemoteConf
from ovos_config.version import NEXT_MAJOR_VERSION

# sentinel to distinguish "not passed" from an explicit falsy value
_unset = object()

from ovos_utils.file_utils import FileWatcher
from ovos_utils.json_helper import flattened_delete, merge_dict
from ovos_utils.log import LOG


def _get_shared_remote_conf(cls):
    """Lazily construct (once) and return the single shared ``RemoteConf``
    instance backing the deprecated ``Configuration.remote`` accessor.

    On ``dev``, ``Configuration.remote`` was a plain class attribute built
    once at class-definition time, so class access and instance access
    always returned the *same* object. ``RemoteConf()`` now warns on every
    construction, so both accessors below must share this one cached
    instance rather than each building their own.
    """
    if cls._remote_instance is None:
        cls._remote_instance = RemoteConf()
    return cls._remote_instance


class _ConfigurationMeta(type):
    """Invalidate the merged-config memo when a layer is swapped, and
    provide a lazily-constructed, deprecated ``Configuration.remote``
    class attribute.

    Tests and embedders replace config layers by direct class-attribute
    assignment (``Configuration.default = LocalConf(...)``,
    ``Configuration.xdg_configs = [...]``) -- a mutation the method-level
    hooks cannot observe. Any class attribute assignment except the memo
    itself drops the memo; spurious invalidations (e.g. assigning ``bus``)
    just cost one rebuild on the next read.

    ``remote`` was removed from the merge stack (OVOS no longer supports
    remote config), but some downstream code still reads
    ``Configuration.remote`` directly. A plain class attribute can't emit a
    DeprecationWarning on access, and constructing ``RemoteConf()`` eagerly
    at class-definition time would warn on every import of this module even
    for callers who never touch ``.remote``. This property defers
    construction (and its warning) until first access.

    Note: a metaclass property is only visible via ``Configuration.remote``
    (class access); instances look up attributes on the class itself, not
    the metaclass, so ``Configuration`` also defines a matching ``remote``
    property for ``Configuration().remote`` (instance access) -- see below.
    Both share ``_get_shared_remote_conf`` so there is only ever one
    ``RemoteConf`` instance, matching dev's single shared object.
    """
    _remote_instance = None

    def __setattr__(cls, name, value):
        super().__setattr__(name, value)
        if name not in ("_merged_cache", "_cache_generation"):
            super().__setattr__("_merged_cache", None)
            super().__setattr__("_cache_generation",
                                cls.__dict__.get("_cache_generation", 0) + 1)

    @property
    def remote(cls):
        return _get_shared_remote_conf(cls)


class Configuration(dict, metaclass=_ConfigurationMeta):
    """Namespace for operations on the configuration singleton."""
    __patch = LocalConf(None)  # Patch config that skills can update to override config
    bus = None
    default = DefaultConfig()
    distribution = DistributionConfig()
    system = SystemConfig()
    assistant = AssistantConfig()  # for runtime changes
    # This includes both the user config and
    # /etc/xdg/mycroft/mycroft.conf, in merge order: the user's own file is
    # last, so it wins over the system-wide XDG dirs
    xdg_configs = [LocalConf(p) for p in get_xdg_config_locations()]
    _watchdog = None
    _callbacks = []
    # Memoized result of load_all_configs() under default constraints.
    # Every mutation path (patch/setitem/update, reload, watchdog file
    # change, remote reload, bus updates) funnels through methods of this
    # class, each of which calls _invalidate_cache() -- so a clean cache is
    # always current. Rebuilding the merge on EVERY key access costs ~75us
    # (dozens of merge_dict calls); constructing one ovos-bus-client Session
    # reads ~13 keys, i.e. ~1 ms of pure re-merging per session, on every
    # utterance, in every OVOS process. The config contract is read-only
    # outside the patch mechanisms (see pop()), which is what makes the
    # shared cached dict safe.
    _merged_cache = None
    # Bumped on every invalidation. An in-flight merge records the generation
    # BEFORE it reads the layers and publishes only if the generation is
    # unchanged -- a mutation that lands mid-merge would otherwise let the
    # finished (stale) merge repopulate the memo.
    _cache_generation = 0

    @property
    def remote(self):
        """DEPRECATED instance-level accessor, mirrors the class-level
        ``_ConfigurationMeta.remote`` property so ``Configuration().remote``
        keeps working exactly like it did on dev, where ``remote`` was a
        plain class attribute reachable from both class and instance."""
        return _get_shared_remote_conf(type(self))

    def __init__(self):
        super().__init__(**self.load_all_configs())

    @staticmethod
    def _invalidate_cache():
        """Drop the memoized merge; the next access rebuilds it."""
        Configuration._merged_cache = None
        Configuration._cache_generation += 1

    @staticmethod
    def _merged():
        """Identity accessor for the memo (internal dict-method fast path)."""
        return Configuration._merged_cache

    @staticmethod
    def _publish_cache(merged, generation):
        """Store a finished merge unless an invalidation landed mid-merge.

        A thread that merged against pre-mutation layer state must not
        repopulate the memo after the mutation cleared it: publish only if
        the generation recorded before the merge is still current. Refusing
        publication just costs the next reader one rebuild.
        """
        if generation == Configuration._cache_generation:
            Configuration._merged_cache = merged

    # dict methods
    def __setitem__(self, key, value):
        Configuration.__patch[key] = value
        Configuration._invalidate_cache()
        super().__setitem__(key, value)
        # sync with other processes connected to bus
        if Configuration.bus:
            # imported from ovos_utils to allow FakeMessage if ovos-bus-client is missing
            from ovos_utils.fakebus import Message
            Configuration.bus.emit(Message("configuration.patch",
                                           {"config": {key: value}}))

    def __getitem__(self, item):
        super().update(Configuration._merged()
                       or Configuration.load_all_configs())
        return super().get(item)

    def __str__(self):
        super().update(Configuration._merged()
                       or Configuration.load_all_configs())
        try:
            return json.dumps(self, sort_keys=True)
        except:
            return super().__str__()

    def __dict__(self):
        super().update(Configuration._merged()
                       or Configuration.load_all_configs())
        return self

    def __repr__(self):
        return self.__str__()

    def __iter__(self):
        super().update(Configuration._merged()
                       or Configuration.load_all_configs())
        for k in super().__iter__():
            yield k

    def update(self, *args, **kwargs):
        Configuration.__patch.update(*args, **kwargs)
        Configuration._invalidate_cache()
        super().update(*args, **kwargs)

    def pop(self, key):
        # we can not pop the key because configs are read only
        # we could do it for __patch but that does not make sense
        # for the object as a whole which is
        # supposed to behave like a python dict
        self.__setitem__(key, None)

    def items(self):
        super().update(Configuration._merged()
                       or Configuration.load_all_configs())
        return super().items()

    def keys(self):
        super().update(Configuration._merged()
                       or Configuration.load_all_configs())
        return super().keys()

    def values(self):
        super().update(Configuration._merged()
                       or Configuration.load_all_configs())
        return super().values()

    # config methods
    @staticmethod
    def load_config_stack(configs=None, cache=_unset, remote=_unset):
        """Load a stack of config dicts into a single dict

        Args:
            configs (list): list of dicts to load
            cache (bool): DEPRECATED and ignored, kept for backwards compatibility
            remote (bool): DEPRECATED and ignored, kept for backwards compatibility.
                OVOS no longer supports remote config, so this is a no-op.
        Returns:
            (dict) merged dict of all configuration files
        """
        warnings.warn(
            f"load_config_stack has been deprecated, use load_all_configs instead. "
            f"will be removed in version {NEXT_MAJOR_VERSION}",
            DeprecationWarning,
            stacklevel=2,
        )
        if cache is not _unset:
            warnings.warn(
                f"the 'cache' argument is deprecated and ignored. "
                f"will be removed in version {NEXT_MAJOR_VERSION}",
                DeprecationWarning,
                stacklevel=2,
            )
        if remote is not _unset:
            warnings.warn(
                f"the 'remote' argument is deprecated and ignored, "
                f"OVOS no longer supports remote config. "
                f"will be removed in version {NEXT_MAJOR_VERSION}",
                DeprecationWarning,
                stacklevel=2,
            )
        if configs:
            return Configuration.filter_and_merge(configs)
        system_constraints = Configuration.get_system_constraints()
        return Configuration.load_all_configs(system_constraints)

    @staticmethod
    def handle_remote_update(message):
        """DEPRECATED: Handler for paired/internet connect.

        OVOS no longer supports remote config, so reloading it has no
        effect on the merged configuration. Kept as a callable no-op shim
        for backwards compatibility; it is not registered as a bus handler.
        """
        warnings.warn(
            f"remote config no longer exists, this is a no-op. "
            f"will be removed in version {NEXT_MAJOR_VERSION}",
            DeprecationWarning,
            stacklevel=2,
        )
        Configuration.remote.reload()

    @staticmethod
    def reset():
        """
        Remove any configuration patches and reload configuration
        """
        Configuration.__patch = {}
        Configuration._invalidate_cache()
        Configuration.reload()

    @staticmethod
    def reload():
        """
        Reload all configuration files
        """
        # invalidate FIRST: if any layer reload below raises after another
        # already succeeded, a memo invalidated only afterwards would keep
        # describing the pre-reload layer state
        Configuration._invalidate_cache()
        Configuration.default.reload()
        Configuration.distribution.reload()
        Configuration.system.reload()
        Configuration.assistant.reload()
        for cfg in Configuration.xdg_configs:
            cfg.reload()
        Configuration._invalidate_cache()

    @staticmethod
    def get_system_constraints() -> dict:
        """
        Get Configuration constraints. Constraints must come from DISTRIBUTION or SYSTEM config.
        If not defined, then load the DEFAULT constraints.
        These settings can not be set anywhere else!
        @return: dict of system configuration constraints
        """

        return Configuration.distribution.get("system") or \
            Configuration.system.get("system") or \
            Configuration.default.get("system") or \
            {}

    @staticmethod
    def load_all_configs(system_constraints: Optional[dict] = None) -> dict:
        """
        Load the stack of config files into a single dict
        @param system_constraints: constraints to limit user config usage
        @return: merged dict of all configuration files
        """
        # Custom constraints bypass the cache entirely (both read and
        # write): the memo is only valid for the default-constraints stack.
        # The public API returns a top-level copy so a caller mutating the
        # result cannot poison the memo (nested values remain shared under
        # the documented read-only contract); the dict methods above use the
        # identity-returning _merged() internally.
        custom_constraints = system_constraints is not None
        generation = Configuration._cache_generation
        if not custom_constraints:
            cached = Configuration._merged()
            if cached is not None:
                return dict(cached)

        # system administrators can define different constraints in how
        # configurations are loaded
        system_constraints = system_constraints or \
                             Configuration.get_system_constraints()
        skip_user = system_constraints.get("disable_user_config", False)

        configs = [Configuration.default, Configuration.distribution, Configuration.system, Configuration.assistant]
        if not skip_user:
            configs += Configuration.xdg_configs

        # runtime patches by skills / bus events
        configs.append(Configuration.__patch)

        # Merge all configs into one
        merged = Configuration.filter_and_merge(configs)
        if not custom_constraints:
            Configuration._publish_cache(merged, generation)
            # same copy-on-return as the hit path: the published memo must
            # never be handed to a caller that could mutate it
            return dict(merged)
        return merged

    @staticmethod
    def filter_and_merge(configs) -> dict:
        """
        Build and return a configuration dict based on configuration files
        @param configs: List of Configuration objects to load
        @return: dict Configuration, built from `configs`
        """
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
        protected_user = protected_keys.get("user") or []
        skip_user = system_conf.get("disable_user_config", False)

        # Merge all configs into one
        base = {}
        for cfg in configs:
            is_user = cfg.path is None or cfg.path not in [Configuration.default.path,
                                                           Configuration.system.path]
            if is_user and skip_user:
                continue
            elif is_user:
                # delete protected keys from user config
                for protection in protected_user:
                    flattened_delete(cfg, protection)
            merge_dict(base, cfg)
        return base

    @staticmethod
    def set_config_update_handlers(bus):
        """
        Setup websocket handlers to update config on emitted changes.
        @param bus: Message bus client instance
        """
        # remove any old event listeners
        Configuration.deregister_bus()

        # attach new bus and listeners
        Configuration.bus = bus
        bus.on("configuration.updated", Configuration.updated)
        bus.on("configuration.patch", Configuration.patch)
        bus.on("configuration.patch.clear", Configuration.patch_clear)
        bus.on("configuration.cache.clear", Configuration.clear_cache)

        Configuration.set_config_watcher()

    @staticmethod
    def set_config_watcher(callback: Optional[callable] = None):
        """
        Setup filewatcher to monitor for config file changes
        @param callback: optional method to call when configuration is changed
        """
        # register the callback before any filesystem I/O so other threads
        # observing Configuration._callbacks see it without racing
        if callback and callback not in Configuration._callbacks:
            Configuration._callbacks.append(callback)
        paths = [Configuration.distribution.path, Configuration.system.path, Configuration.assistant.path] + \
                [c.path for c in Configuration.xdg_configs]
        if not Configuration._watchdog:
            # Watch every configuration path, including the ones that do not
            # exist yet: a device that has never been configured has no user
            # config, and the first write to it is the one write it is certain
            # to make. FileWatcher watches the parent directory and filters by
            # name, and declines on its own when that directory is missing.
            Configuration._watchdog = FileWatcher(
                paths,
                Configuration._on_file_change
            )

    @staticmethod
    def _on_file_change(path: str):
        """
        Callback method for FileWatcher
        @param path: Configuration file path reporting a change
        """
        # reload updated config
        for cfg in Configuration.xdg_configs + [Configuration.distribution,
                                                Configuration.system,
                                                Configuration.assistant]:
            if cfg.path == path:
                old_cfg = hash(cfg)
                try:
                    cfg.reload()
                except Exception as e:
                    # Filewatcher only calls this on file close, so this
                    # is really an error
                    LOG.exception(f"Failed to load: {path}: {e}")

                new_cfg = hash(cfg)
                if old_cfg == new_cfg:
                    LOG.info(f"{path} unchanged")
                    return
                break
        else:
            LOG.debug(f"Ignoring non-config file change: {path}")
            return

        Configuration._invalidate_cache()
        LOG.info(f'{path} changed on disk')
        LOG.debug(f"Calling {len(Configuration._callbacks)} callbacks")
        for handler in Configuration._callbacks:
            try:
                handler()
            except:
                LOG.exception("Error in config update callback handler")

    @staticmethod
    def deregister_bus():
        """
        Remove messagebus handlers for configuration updates
        """
        if Configuration.bus:
            Configuration.bus.remove("configuration.updated",
                                     Configuration.updated)
            Configuration.bus.remove("configuration.patch",
                                     Configuration.patch)
            Configuration.bus.remove("configuration.patch.clear",
                                     Configuration.patch_clear)
            Configuration.bus.remove("configuration.cache.clear",
                                     Configuration.clear_cache)

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
        Configuration._invalidate_cache()

    @staticmethod
    def patch_clear(message):
        """Clear the config patch space.

        Args:
            message: Messagebus message should contain a config
                     in the data payload.
        """
        Configuration.__patch = {}
        Configuration._invalidate_cache()

    # Backwards compat methods
    @staticmethod
    def clear_cache(message=None):
        """Drop the memoized merged config and reload from disk."""
        Configuration._invalidate_cache()
        Configuration.updated(message)


def update_assistant_config(config, bus=None):
    """updates the assistant config file (ASSISTANT_CONFIG / runtime.conf)
    with the contents of the provided dict"""
    conf = Configuration.assistant
    conf.merge(config)
    conf.store()
    if bus:  # inform all Configuration objects connected to the bus
        # imported from ovos_utils to allow FakeMessage if ovos-bus-client is missing
        from ovos_utils.fakebus import Message
        bus.emit(Message("configuration.patch", {"config": config}))
    return conf


def read_mycroft_config():
    """ returns a stateless dict with the loaded configuration """
    warnings.warn(
        f"read_mycroft_config has been deprecated, use 'Configuration()' directly. "
        f"will be removed in version {NEXT_MAJOR_VERSION}",
        DeprecationWarning,
        stacklevel=2,
    )
    return dict(Configuration())


def update_mycroft_config(config, path=None, bus=None):
    """ updates user config file with the contents of provided dict
    if a path is provided that location will be used instead of UserConfig"""
    warnings.warn(
        f"update_mycroft_config has been deprecated, use 'update_assistant_config' instead. "
        f"will be removed in version {NEXT_MAJOR_VERSION}",
        DeprecationWarning,
        stacklevel=2,
    )
    if path is None:
        conf = UserConfig()
    else:
        conf = LocalConf(path)
    conf.merge(config)
    conf.store()
    if bus:  # inform all Configuration objects connected to the bus
        # imported from ovos_utils to allow FakeMessage if ovos-bus-client is missing
        from ovos_utils.fakebus import Message
        bus.emit(Message("configuration.patch", {"config": config}))
    return conf
