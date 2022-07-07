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
import re
from os.path import exists, isfile

import yaml

from ovos_config.locations import USER_CONFIG, SYSTEM_CONFIG, WEB_CONFIG_CACHE, DEFAULT_CONFIG
from ovos_utils import camel_case_split
from ovos_utils.json_helper import load_commented_json, merge_dict
from ovos_utils.log import LOG

try:
    import mycroft.api as selene_api
except ImportError:
    # TODO https://github.com/OpenVoiceOS/selene_api
    selene_api = None


def is_remote_list(values):
    """Check if list corresponds to a backend formatted collection of dicts
    """
    for v in values:
        if not isinstance(v, dict):
            return False
        if "@type" not in v.keys():
            return False
    return True


def translate_remote(config, setting):
    """Translate config names from server to equivalents for mycroft-core.

    Args:
        config:     base config to populate
        settings:   remote settings to be translated
    """
    IGNORED_SETTINGS = ["uuid", "@type", "active", "user", "device"]

    for k, v in setting.items():
        if k not in IGNORED_SETTINGS:
            # Translate the CamelCase values stored remotely into the
            # Python-style names used within mycroft-core.
            key = re.sub(r"Setting(s)?", "", k)
            key = camel_case_split(key).replace(" ", "_").lower()
            if isinstance(v, dict):
                config[key] = config.get(key, {})
                translate_remote(config[key], v)
            elif isinstance(v, list):
                if is_remote_list(v):
                    if key not in config:
                        config[key] = {}
                    translate_list(config[key], v)
                else:
                    config[key] = v
            else:
                config[key] = v


def translate_list(config, values):
    """Translate list formatted by mycroft server.

    Args:
        config (dict): target config
        values (list): list from mycroft server config
    """
    for v in values:
        module = v["@type"]
        if v.get("active"):
            config["module"] = module
        config[module] = config.get(module, {})
        translate_remote(config[module], v)


class LocalConf(dict):
    """Config dictionary from file."""
    allow_overwrite = True

    def __init__(self, path):
        super().__init__(self)
        self.path = path
        if path:
            self.load_local(path)

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
        """Load local json file into self.

        Args:
            path (str): file to load
        """
        path = path or self.path
        if not path:
            LOG.error(f"in memory configuration, nothing to load")
            return
        if exists(path) and isfile(path):
            try:
                if self._get_file_format(path) == "yaml":
                    with open(path) as f:
                        config = yaml.safe_load(f)
                else:
                    config = load_commented_json(path)
                for key in config:
                    self.__setitem__(key, config[key])
                LOG.debug(f"Configuration {path} loaded")
            except Exception as e:
                LOG.exception(f"Error loading configuration '{path}'")
        else:
            LOG.debug(f"Configuration '{path}' not defined, skipping")

    def reload(self):
        self.load_local(self.path)

    def store(self, path=None):
        """Cache the received settings locally.

        The cache will be used if the remote is unreachable to load settings
        that are as close to the user's as possible.
        """
        path = path or self.path
        if not path:
            LOG.error(f"in memory configuration, no save location")
            return
        if self._get_file_format(path) == "yaml":
            with open(path, 'w') as f:
                yaml.dump(dict(self), f, allow_unicode=True,
                          default_flow_style=False, sort_keys=False)
        else:
            with open(path, 'w') as f:
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


class MycroftSystemConfig(ReadOnlyConfig):
    def __init__(self, allow_overwrite=False):
        super().__init__(SYSTEM_CONFIG, allow_overwrite)


class RemoteConf(LocalConf):
    """Config dictionary fetched from mycroft.ai."""

    def __init__(self, cache=WEB_CONFIG_CACHE):
        super(RemoteConf, self).__init__(cache)

    def reload(self):
        if selene_api is None:
            self.load_local(self.path)
            return
        try:
            if not selene_api.is_paired():
                self.load_local(self.path)
                return

            if selene_api.is_backend_disabled():
                # disable options that require backend
                config = {
                    "server": {
                        "metrics": False,
                        "sync_skill_settings": False
                    },
                    "skills": {"upload_skill_manifest": False},
                    "opt_in": False
                }
                for key in config:
                    self.__setitem__(key, config[key])
            else:
                api = selene_api.DeviceApi()
                setting = api.get_settings()
                location = None
                try:
                    location = api.get_location()
                except Exception as e:
                    LOG.error(f"Exception fetching remote location: {e}")
                    if exists(self.path) and isfile(self.path):
                        location = load_commented_json(self.path).get('location')

                if location:
                    setting["location"] = location
                # Remove server specific entries
                config = {}
                translate_remote(config, setting)

                for key in config:
                    self.__setitem__(key, config[key])
                self.store(self.path)

        except Exception as e:
            LOG.error(f"Exception fetching remote configuration: {e}")
            self.load_local(self.path)


class MycroftUserConfig(LocalConf):
    def __init__(self):
        super().__init__(USER_CONFIG)


MycroftXDGConfig = MycroftUserConfig
