"""This file will check env vars and determine ovos config file locations

this info is used to determine the default XDG paths and default config file location

OVOS_CONFIG_BASE_FOLDER - mycroft
OVOS_CONFIG_FILENAME - mycroft.conf
OVOS_DEFAULT_CONFIG - full path to default mycroft.conf
"""
import os
from os.path import dirname


def get_ovos_config():
    """
    `base_folder`, `config_filename` and "default_config_path" are overridden by envvars
    `OVOS_CONFIG_BASE_FOLDER`,`OVOS_CONFIG_FILENAME` and `OVOS_DEFAULT_CONFIG`, respectively.
    """
    # let's check for os.env overrides, those take precedence over default values
    return {"base_folder": os.environ.get("OVOS_CONFIG_BASE_FOLDER") or "mycroft",
            "config_filename": os.environ.get("OVOS_CONFIG_FILENAME") or "mycroft.conf",
            "default_config_path": os.environ.get("OVOS_DEFAULT_CONFIG") or f"{dirname(__file__)}/mycroft.conf"}


def save_ovos_config(new_config):
    """DEPRECATED - ovos.conf no longer used"""
    from ovos_utils.log import LOG
    LOG.warning("ovos.conf file has been deprecated! this method will be removed in next stable release")
    return


def get_ovos_default_config_paths():
    """DEPRECATED - ovos.conf no longer used"""
    from ovos_utils.log import LOG
    LOG.warning("ovos.conf file has been deprecated! this method will be removed in next stable release")
    return []


def is_using_xdg():
    """ BACKWARDS COMPAT: logs warning and always returns True"""
    from ovos_utils.log import LOG
    LOG.warning(
        "is_using_xdg has been deprecated! XDG specs are always honoured, "
        "this method will be removed in next stable release")
    return True


def get_xdg_base():
    """ base folder name to be used when building paths of the format {$XDG_XXX}/{base}

    different derivative cores may change this folder, this value is derived from ovos.conf
        eg, "mycroft", "hivemind", "neon" ....
    """
    return get_ovos_config().get("base_folder") or "mycroft"


def set_xdg_base(folder_name):
    """ base folder name to be used when building paths of the format {$XDG_XXX}/{base}

    different derivative cores may change this folder, this value is derived from ovos.conf
        eg, "mycroft", "hivemind", "neon" ....

    NOTE: this value will be set globally, per core overrides in ovos.conf take precedence
    """
    from ovos_utils.log import LOG
    LOG.info(f"XDG base folder set to: '{folder_name}'")
    os.environ["OVOS_CONFIG_BASE_FOLDER"] = folder_name


def set_config_filename(file_name, core_folder=None):
    """ base config file name to be used when building paths

    different derivative cores may change this filename, this value is derived from ovos.conf
        eg, "mycroft.conf", "hivemind.json", "neon.yaml" ....

    NOTE: this value will be set globally, per core overrides in ovos.conf take precedence
    """
    from ovos_utils.log import LOG

    if core_folder:
        set_xdg_base(core_folder)
    LOG.info(f"config filename set to: '{file_name}'")
    os.environ["OVOS_CONFIG_FILENAME"] = file_name


def get_config_filename():
    """ base config file name to be used when building paths

    different derivative cores may change this filename, this value is derived from ovos.conf
        eg, "mycroft.conf", "hivemind.json", "neon.yaml" ....
    """
    return get_ovos_config().get("config_filename") or "mycroft.conf"


def set_default_config(file_path=f"{dirname(__file__)}/mycroft.conf"):
    """ full path to default config file to be used
    NOTE: this is a full path, not a directory! "config_filename" parameter is not used here

    different derivative cores may change this file, this value is derived from ovos.conf

    NOTE: this value will be set globally, per core overrides in ovos.conf take precedence
    """
    from ovos_utils.log import LOG

    LOG.info(f"default config file changed to: {file_path}")
    os.environ["OVOS_DEFAULT_CONFIG"] = file_path
