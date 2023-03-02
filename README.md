[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE.md) 
![Unit Tests](https://github.com/OpenVoiceOS/ovos-core/actions/workflows/unit_tests.yml/badge.svg)
[![codecov](https://codecov.io/gh/OpenVoiceOS/ovos-config/branch/dev/graph/badge.svg?token=CS7WJH4PO2)](https://codecov.io/gh/OpenVoiceOS/ovos-config)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)
[![Chat](https://img.shields.io/matrix/openvoiceos-general:matrix.org)](https://matrix.to/#/#OpenVoiceOS-general:matrix.org)
[![GitHub Discussions](https://img.shields.io/github/discussions/OpenVoiceOS/OpenVoiceOS?label=OVOS%20Discussions)](https://github.com/OpenVoiceOS/OpenVoiceOS/discussions)

# OVOS-config

helper package to interact with mycroft config

## Command Line usage

A small helper tool is included to quickly show, get or set config values

<img width="1214" alt="ovos-config" src="https://user-images.githubusercontent.com/25036977/219516755-b454f28f-2a34-4caf-a91f-6182ff68049a.png">

Quick rundown (cli):

* `ovos-config get`
  
  * Loose search (search a key or parts therof):\
  \
Given an entry of

        {'PHAL': {
                'ovos-PHAL-plugin-system': {
                        'enabled': True
                },
                'ovos-PHAL-plugin-connectivity-events': {
                        'enabled': True
                },
                ... 
        }

    `ovos-config get -k phal` would yield  **all**  PHAL entries and present it to the user (and the path where they were found)


  * Strict search (search keys in a distinct location): 

    `ovos-config get -k /PHAL/ovos-PHAL-plugin-system/enabled` 

    This will output only the value or exit out if no key is found (root slash indicating a strict search)

* `ovos-config set` 

  * Searches loosly for keys containing the query string and presents a choice to the user to define a value

    `ovos-config set -k phal`
    
    <img width="423" alt="ovos-config2" src="https://user-images.githubusercontent.com/25036977/219526126-dfc547e7-6110-461a-92ba-83e850d03c70.png">

    The type is derived from the joined config and thus can be safely cast into the user conf.\
    Optionally a value (`-v`) can be sent as an argument.

* `ovos-config show` 

  * Get a full table of either the joined, user (`-u`), system (`-s`) or remote (`-r`) configuration.
    This can be further refined by passing a `--section`, which can be listed with `ovos-config show -l`

&nbsp;
--------------
&nbsp;

## Configuration Structure

### ovos.conf
The `ovos_config` package determines which config files to load based on `ovos.conf`.
`get_ovos_config` will return default values that load `mycroft.conf` unless otherwise configured.

`ovos.conf` files are loaded in the following order, with later files taking priority over earlier ones in the list:
1. /etc/OpenVoiceOS/ovos.conf
2. /etc/mycroft/ovos.conf (Deprecated)
3. `XDG_CONFIG_DIRS` + /OpenVoiceOS/ovos.conf
3. /etc/xdg/OpenVoiceOS/ovos.conf
4. `XDG_CONFIG_HOME` (default ~/.config) + /OpenVoiceOS/ovos.conf

A simple `ovos_config` should have a structure like:

```json
{
"base_folder": "mycroft",
"config_filename": "mycroft.conf",
"default_config_path": "<Absolute Path to Installed Core>/configuration/mycroft.conf",
"module_overrides": {},
"submodule_mappings": {}
}
```
>*Note*: `default_config_path` should always be an absolute path. This is generally
detected automatically, but any manual override must specify an absolute path to a json or yaml config file.

Non-Mycroft modules may specify alternate config paths. A call to `get_ovos_config` from 
`neon_core` or `neon_messagebus` will return a configuration like:

```json
{
  "base_folder": "neon",
  "config_filename": "neon.yaml",
  "default_config_path": "/etc/example/config/neon.yaml",
  "module_overrides": {
    "neon_core": {
      "base_folder": "neon",
      "config_filename": "neon.yaml",
      "default_config_path": "/etc/example/config/neon.yaml"
    }
  },
  "submodule_mappings": {
    "neon_core.skills.skill_manager": "neon_core",
    "neon_messagebus": "neon_core",
    "neon_speech": "neon_core",
    "neon_audio": "neon_core",
    "neon_gui": "neon_core"
  }
}
```

If `get_ovos_config` was called from `mycroft` with the same configuration file as the last example,
the returned configuration would be:

```json
{
  "base_folder": "mycroft",
  "config_filename": "mycroft.conf",
  "default_config_path": "<Path to Installed Core>/configuration/mycroft.conf",
  "module_overrides": {
    "neon_core": {
      "base_folder": "neon",
      "config_filename": "neon.yaml",
      "default_config_path": "/etc/example/config/neon.yaml"
    }
  },
  "submodule_mappings": {
    "neon_core.skills.skill_manager": "neon_core",
    "neon_messagebus": "neon_core",
    "neon_speech": "neon_core",
    "neon_audio": "neon_core",
    "neon_gui": "neon_core"
  }
}
```

## Configuration
`ovos_config.config.Configuration` is a singleton object that loads a single config
object. The configuration files loaded are determined by `ovos.conf` as described above.
Using the above example, if `Configuration()` is called from `neon_speech`, the
following configs would be loaded in this order:

1. /etc/example/config/neon.yaml
2. `os.environ.get('MYCROFT_SYSTEM_CONFIG')` or /etc/neon/neon.yaml
3. `os.environ.get('MYCROFT_WEB_CACHE')` or `XDG_CONFIG_PATH`/neon/web_cache.json (unless `disable_remote_config == True` in earlier config)
4. ~/.neon/neon.yaml (Deprecated)
3. `XDG_CONFIG_DIRS` + /neon/neon.yaml
3. /etc/xdg/neon/neon.yaml
4. `XDG_CONFIG_HOME` (default ~/.config) + /neon/neon.yaml

### Configuring Configuration
There are a couple of special configuration keys that change the way the configuration stack loads.

* `Default` config refers to the config specified at `default_config_path` in 
`ovos.conf` (#1 `/etc/example/config/neon.yaml` in the stack above).
* `System` config refers to the config at `/etc/{base_folder}/{config_filename}` (#2 `/etc/neon/neon.yaml` in the stack above).

#### protected_keys
A `"protected_keys"` configuration section may be added to a `Default` or `System` Config file
(default `/etc/mycroft/mycroft.conf`). This configuration section specifies 
other configuration keys that may not be specified in `remote` or `user` configurations.
Keys may specify nested parameters with `.` to exclude specific keys within nested dictionaries.
An example config could be:

```json
{
  "protected_keys": {
    "remote": [
      "gui_websocket.host",
      "websocket.host"
    ],
    "user": [
      "gui_websocket.host"
    ]
  }
}
```
This example specifies that `config['gui_websocket']['host']` may be specified in user configuration, but not remote.
`config['websocket']['host']` may not be specified in user or remote config, so it will only consider default
and system configurations.

#### disable_user_config
If this config parameter is set to True in `Default` or `System` configuration, 
no user configurations will be loaded (no XDG configuration paths).

#### disable_remote_config
If this config parameter is set to True in `Default` or `System` configuration, 
the remote configuration (`web_cache.json`) will not be loaded.
