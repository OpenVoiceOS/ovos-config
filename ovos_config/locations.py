# Copyright 2018 Mycroft AI Inc.
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
import os
import warnings
from os.path import join, dirname, exists, isfile
from time import sleep
import ovos_config.meta as _ovos_config
from ovos_utils.xdg_utils import xdg_config_dirs, xdg_config_home, xdg_data_dirs, xdg_data_home, xdg_cache_home


def get_xdg_config_dirs(folder=None):
    """ return list of possible XDG config dirs taking into account ovos.conf """
    folder = folder or _ovos_config.get_xdg_base()
    xdg_dirs = xdg_config_dirs() + [xdg_config_home()]
    return [join(path, folder) for path in xdg_dirs]


def get_xdg_data_dirs(folder=None):
    """ return list of possible XDG data dirs taking into account ovos.conf """
    folder = folder or _ovos_config.get_xdg_base()
    return [join(path, folder) for path in xdg_data_dirs()]


def get_xdg_config_save_path(folder=None):
    """ return base XDG config save path taking into account ovos.conf """
    folder = folder or _ovos_config.get_xdg_base()
    return join(xdg_config_home(), folder)


def get_xdg_data_save_path(folder=None):
    """ return base XDG data save path taking into account ovos.conf """
    folder = folder or _ovos_config.get_xdg_base()
    return join(xdg_data_home(), folder)


def get_xdg_cache_save_path(folder=None):
    """ return base XDG cache save path taking into account ovos.conf """
    folder = folder or _ovos_config.get_xdg_base()
    return join(xdg_cache_home(), folder)


def find_user_config():
    """ return user config full file path taking into account ovos.conf """
    path = join(get_xdg_config_save_path(), _ovos_config.get_config_filename())
    if isfile(path):
        return path
    old, path = get_config_locations(default=False, web_cache=False,
                                     distribution=False, system=False,
                                     old_user=True, user=True)
    if isfile(path):
        return path
    if isfile(old):
        return old
    return path


def get_config_locations(default=True, web_cache=True, distribution=True,
                         system=True, old_user=True, user=True):
    """return list of all possible config files paths sorted by priority taking into account ovos.conf"""
    locs = []
    ovos_cfg = _ovos_config.get_ovos_config()
    if default:
        locs.append(ovos_cfg["default_config_path"])
    if distribution:
        locs.append(f"/usr/share/{ovos_cfg['base_folder']}/{ovos_cfg['config_filename']}")
    if system:
        locs.append(f"/etc/{ovos_cfg['base_folder']}/{ovos_cfg['config_filename']}")
    if web_cache:
        locs.append(get_webcache_location())
    if old_user:
        locs.append(f"~/.{ovos_cfg['base_folder']}/{ovos_cfg['config_filename']}")
    if user:
        locs.append(f"{get_xdg_config_save_path()}/{ovos_cfg['config_filename']}")
    return locs


def get_webcache_location():
    """ return remote config cache full file path taking into account ovos.conf """
    warnings.warn(
        "deprecated without replacement, OVOS no longer supports remote config",
        DeprecationWarning,
        stacklevel=2,
    )
    return join(get_xdg_config_save_path(), 'web_cache.json')


def get_xdg_config_locations():
    """ return list of possible XDG config full file paths taking into account ovos.conf """
    # This includes both the user config and
    # /etc/xdg/mycroft/mycroft.conf
    xdg_paths = list(reversed(
        [join(p, _ovos_config.get_config_filename())
         for p in get_xdg_config_dirs()]
    ))
    return xdg_paths


def find_default_config():
    """return the bundled file in ovos_config package"""
    warnings.warn(
        "use 'from ovos_config.locations import USER_CONFIG'",
        DeprecationWarning,
        stacklevel=2,
    )
    return join(dirname(__file__), "mycroft.conf")


DEFAULT_CONFIG = _ovos_config.get_ovos_config()['default_config_path']
DISTRIBUTION_CONFIG = os.environ.get('OVOS_DISTRIBUTION_CONFIG',
                               f'/usr/share/{_ovos_config.get_xdg_base()}/'
                               f'{_ovos_config.get_config_filename()}')
SYSTEM_CONFIG = os.environ.get('MYCROFT_SYSTEM_CONFIG',
                               f'/etc/{_ovos_config.get_xdg_base()}/'
                               f'{_ovos_config.get_config_filename()}')
USER_CONFIG = join(get_xdg_config_save_path(), _ovos_config.get_config_filename())
ASSISTANT_CONFIG = join(get_xdg_config_save_path(), "runtime.conf") # for plugins/skills to store changes
WEB_CONFIG_CACHE = os.environ.get('MYCROFT_WEB_CACHE') or \
                   get_webcache_location()


def __ensure_folder_exists(path):
    """ Make sure the directory for the specified path exists.

        Args:
            path (str): path to config file
     """
    directory = dirname(path)
    if not exists(directory):
        try:
            os.makedirs(directory)
        except:
            sleep(0.2)
            if not exists(directory):
                try:
                    os.makedirs(directory)
                except Exception as e:
                    pass

__ensure_folder_exists(USER_CONFIG)
