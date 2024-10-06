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

  * Searches loosely for keys containing the query string and presents a choice to the user to define a value

    `ovos-config set -k phal`
    
    <img width="423" alt="ovos-config2" src="https://user-images.githubusercontent.com/25036977/219526126-dfc547e7-6110-461a-92ba-83e850d03c70.png">

    The type is derived from the joined config and thus can be safely cast into the user conf.\
    Optionally a value (`-v`) can be sent as an argument.


* `ovos-config autoconfigure`
  
![image](https://github.com/user-attachments/assets/7a39707e-ac56-498c-a269-337f4de88442)

![image](https://github.com/user-attachments/assets/01ee6b46-c3c2-4fd9-b048-5fe3f074f031)


* `ovos-config show` 

  * Get a full table of either the joined, user (`-u`), system (`-s`) or remote (`-r`) configuration.
    This can be further refined by passing a `--section`, which can be listed with `ovos-config show -l`
