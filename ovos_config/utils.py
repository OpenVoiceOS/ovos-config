import json
import importlib

from typing import Optional
from ovos_utils.log import LOG
from os import makedirs
from os.path import join, dirname
from ovos_utils.xdg_utils import xdg_config_home
# backwards compat
from ovos_utils.file_utils import FileWatcher, FileEventHandler


def init_module_config(module_name: str, module_override: str,
                       module_config: Optional[dict] = None):
    """
    Configure a module to use a configured override
    @param module_name: module to configure
    @param module_override: key in `module_overrides` to assign to `module_name`
    @param module_config: configuration for the specified module_override
    """
    from ovos_config.meta import get_ovos_config
    ovos_conf = get_ovos_config()
    ovos_conf.setdefault('module_overrides', {})
    ovos_conf.setdefault('submodule_mappings', {})

    config_updated = False

    # Check for and update module_overrides
    existing_config = ovos_conf['module_overrides'].get(module_override)
    if module_config:
        if existing_config and module_config != existing_config:
            LOG.info(f"existing={existing_config}")
            LOG.warning(f"requested={module_override}")
            raise RuntimeError("Passed configuration conflicts with existing")
        elif not existing_config:
            LOG.info(f"Configuring {module_override} config")
            ovos_conf['module_overrides'][module_override] = module_config
            config_updated = True

    # Check for and update submodules
    if module_name == "__main__":
        raise ValueError(f"Configuring `__main__` has unintended consequences"
                         f"and is not supported here")
    if module_name in ovos_conf['submodule_mappings']:
        LOG.debug(f"{module_name} already configured, skipping configuration")
    else:
        ovos_conf["submodule_mappings"][module_name] = module_override
        config_updated = True

    # Check if ovos config is modified
    if not config_updated:
        LOG.debug("Configuration unchanged")
        return

    ovos_path = join(xdg_config_home(), "OpenVoiceOS", "ovos.conf")
    makedirs(dirname(ovos_path), exist_ok=True)
    config_to_write = {
        "module_overrides": ovos_conf.get('module_overrides'),
        "submodule_mappings": ovos_conf.get('submodule_mappings')
    }
    LOG.info(f"Updating configuration at: {ovos_path}")
    with open(ovos_path, "w+") as f:
        json.dump(config_to_write, f, indent=4)

    # Note that the below block reloads modules in a specific order due to
    # imports within ovos_config and mycroft.configuration
    import ovos_config
    importlib.reload(ovos_config.locations)  # Reset global config paths
    # from ovos_config.meta import get_ovos_config
    ovos_conf = get_ovos_config()  # Load the full stack for /etc overrides

    module_default_config = ovos_conf["module_overrides"][module_override].get(
        "default_config_path")
    if module_default_config \
            and ovos_config.locations.DEFAULT_CONFIG != module_default_config:
        ovos_config.locations.DEFAULT_CONFIG = module_default_config

        # Default config changed, remove any cached configuration
        del ovos_config.config.Configuration
        del ovos_config.Configuration

    import ovos_config.models
    importlib.reload(ovos_config.models)
    importlib.reload(ovos_config.config)
    importlib.reload(ovos_config)
