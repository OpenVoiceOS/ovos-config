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
import yaml

from time import time
from os.path import exists, isfile, getmtime
from combo_lock import NamedLock
from ovos_utils.json_helper import load_commented_json, merge_dict
from ovos_utils.log import LOG

from ovos_config.locations import USER_CONFIG, DISTRIBUTION_CONFIG, SYSTEM_CONFIG, WEB_CONFIG_CACHE, DEFAULT_CONFIG


class LocalConf(dict):
    """Config dictionary from file."""
    allow_overwrite = True
    # lock is shared among all subclasses,
    # regardless of what file is being edited only one file should change at a time
    # this ensures orderly behaviour in anything monitoring changes,
    #   eg FileWatcher util, configuration.patch bus handlers
    __lock = NamedLock("ovos_config")

    def __init__(self, path):
        super().__init__(self)
        self.path = path
        self._last_loaded = None
        if path:
            self.load_local(path)

    def __hash__(self):
        return hash(json.dumps(dict(self), sort_keys=True))

    def _get_file_format(self, path=None):
        """The config file format
        supported file extensions:
        - json (.json)
        - commented json (.conf)
        - yaml (.yaml/.yml)

        returns "yaml" or "json"
        """
        path = path or self.path
        if not path:
            return "dict"
        if path.endswith(".yml") or path.endswith(".yaml"):
            return "yaml"
        else:
            return "json"

    def load_local(self, path=None):
        """
        Load local json file into self.

        Args:
            path (str): file to load
        """
        path = path or self.path
        if not path:
            LOG.error("in memory configuration, nothing to load")
            return
        if exists(path) and isfile(path):
            with self.__lock:
                try:
                    if self._get_file_format(path) == "yaml":
                        with open(path, encoding="utf-8") as f:
                            config = yaml.safe_load(f)
                    else:
                        config = load_commented_json(path)
                    if config:
                        for key in config:
                            self.__setitem__(key, config[key])
                        LOG.debug(f"Configuration {path} loaded")
                    else:
                        LOG.debug(f"Empty config found at: {path}")
                except Exception as e:
                    LOG.exception(f"Error loading configuration '{path}'")
                if path == self.path and isfile(self.path):
                    self._last_loaded = getmtime(self.path)
        else:
            LOG.debug(f"Configuration '{path}' not defined, skipping")

    def reload(self):
        if isfile(self.path) \
            and self._last_loaded \
            and self._last_loaded == getmtime(self.path):
            LOG.debug(f"{self.path} not changed since last load "
                      f"(changed {time() - self._last_loaded} seconds ago)")
            return
        self.load_local(self.path)

    def store(self, path=None):
        path = path or self.path
        if not path:
            LOG.error("in memory configuration, no save location")
            return
        with self.__lock:
            if self._get_file_format(path) == "yaml":
                with open(path, 'w+', encoding="utf-8") as f:
                    yaml.dump(dict(self), f, allow_unicode=True,
                              default_flow_style=False, sort_keys=False)
            else:
                with open(path, 'w+', encoding="utf-8") as f:
                    json.dump(self, f, indent=2)

    def merge(self, conf):
        merge_dict(self, conf)


class ReadOnlyConfig(LocalConf):
    """ read only  """

    def __init__(self, path, allow_overwrite=False):
        super().__init__(path)
        self.allow_overwrite = allow_overwrite

    def reload(self):
        old = self.allow_overwrite
        self.allow_overwrite = True
        super().reload()
        self.allow_overwrite = old

    def __setitem__(self, key, value):
        if not self.allow_overwrite:
            raise PermissionError(f"{self.path} is read only! it can not be modified at runtime")
        super().__setitem__(key, value)

    def merge(self, *args, **kwargs):
        if not self.allow_overwrite:
            raise PermissionError(f"{self.path} is read only! it can not be modified at runtime")
        super().merge(*args, **kwargs)

    def store(self, path=None):
        if not self.allow_overwrite:
            raise PermissionError(f"{self.path} is read only! it can not be modified at runtime")
        super().store(path)


class MycroftDefaultConfig(ReadOnlyConfig):
    def __init__(self):
        super().__init__(DEFAULT_CONFIG)

    def set_root_config_path(self, root_config):
        # in case we got it wrong / non standard
        self.path = root_config
        self.reload()


class OvosDistributionConfig(ReadOnlyConfig):
    def __init__(self, allow_overwrite=False):
        super().__init__(DISTRIBUTION_CONFIG, allow_overwrite)


class MycroftSystemConfig(ReadOnlyConfig):
    def __init__(self, allow_overwrite=False):
        super().__init__(SYSTEM_CONFIG, allow_overwrite)


class RemoteConf(LocalConf):
    """Config dictionary fetched from the backend
    It's a local file expected to be managed by an external service"""

    def __init__(self, cache=WEB_CONFIG_CACHE):
        super(RemoteConf, self).__init__(cache)


class MycroftUserConfig(LocalConf):
    def __init__(self):
        super().__init__(USER_CONFIG)


MycroftXDGConfig = MycroftUserConfig
