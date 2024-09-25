#!/bin/env python3
import json
import os.path
from typing import Any, Tuple

import rich_click as click
from rich import print_json
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

from ovos_config import Configuration, LocalConf
from ovos_config.locations import USER_CONFIG

CONFIG = Configuration()
CONFIGS = [("Joined", CONFIG),
           ("Sytem", CONFIG.system),
           ("User", LocalConf(USER_CONFIG)),
           ("Remote", CONFIG.remote)]
SECTIONS = [k for k, v in CONFIG.items() if isinstance(v, dict)] + ["base"]


def drawTable(dic: dict, table: Table, level: int = 0) -> None:
    for key, value in dic.items():
        s = f'{key:>{4 * level + len(key)}}'
        if not isinstance(value, dict):
            table.add_row(s, str(value))
        else:
            if level == 0:
                table.add_section()
            table.add_row(f'[red]{s}[/red]')
            drawTable(value, table, level + 1)
    return


def dictDepth(dic: dict, level: int = 1) -> int:
    if not isinstance(dic, dict) or not dic:
        return level
    return max(dictDepth(dic[key], level + 1)
               for key in dic)


def walkDict(dic: dict,
             key: str,
             full_path: bool = False,
             path: Tuple = (),
             found: bool = False):
    for k in dic.keys():
        if key.lower() in k.lower():
            found = True
            if not full_path:
                yield path + (k,), dic[k]
                found = False

        # endpoint
        if type(dic[k]) != dict:
            if found:
                yield path + (k,), dic[k]
        else:
            yield from walkDict(dic[k],
                                key,
                                full_path,
                                path + (k,),
                                found)
        found = False


def pathGet(dic: dict, path: str) -> Any:
    path = path.lstrip("/")
    for item in path.split("/"):
        dic = dic[item]
    return dic


def pathSet(dic: dict, path: str, value: Any) -> None:
    _path = path.lstrip("/").split("/")
    _key = _path.pop(-1)
    for entry in _path:
        if entry not in dic:
            dic[entry] = {}
        dic = dic[entry]
    dic[_key] = value


click.rich_click.STYLE_ARGUMENT = "dark_red"
click.rich_click.STYLE_OPTION = "dark_red"
click.rich_click.STYLE_SWITCH = "indian_red"
click.rich_click.COMMAND_GROUPS = {
    "ovos-config": [
        {
            "name": "Show configuration tables (Joined/User/System/Remote)",
            "commands": ["show"],
            "table_styles": {
                "row_styles": ["white"],
                "padding": (0, 2),
                "title_justify": "left"
            },
        },
        {
            "name": "Get specific key(s)",
            "commands": ["get"],
            "table_styles": {
                "row_styles": ["white"],
                "padding": (0, 2),
            },
        },
        {
            "name": "Setting user values",
            "commands": ["set"],
            "table_styles": {
                "row_styles": ["white"],
                "padding": (0, 3),
            },
        },
    ]
}

console = Console()


@click.group()
def config():
    """\b
    Small helper tool to quickly show, get or set config values

    `ovos-config [COMMAND] --help` for further information about the specific command ARGUMENTS
    \b
    """
    pass


@config.command()
@click.option("--lang", "-l", required=True, help="the language code")
@click.option("--online", "-on", is_flag=True, help="set default online STT plugin")
@click.option("--offline", "-off", is_flag=True, help="set default offline STT plugin")
@click.option("--male", "-m", is_flag=True, help="set default male voice for TTS")
@click.option("--female", "-f", is_flag=True, help="set default female voice for TTS")
def autoconfigure(lang, online, offline, male, female):
    """
Automatically configures the language, STT, and TTS settings based on user input.

sets up configurations for language, online or offline speech-to-text, and male or female text-to-speech voice options.

ensures that only one of the mutually exclusive options (online/offline and male/female) is selected, and merges the appropriate configuration files for the selected options.

Notes:

    - If neither `online` nor `offline` are provided, defaults to `online`.

    - If neither `male` nor `female` are provided, TTS configuration is skipped.

    - The function merges configuration files based on the specified options and stores the final configuration in the user's config file.
"""
    if not online and not offline:
        console.print("[red]Defaulting to online public servers[/red]")
        online = True

    if online and offline:
        raise click.UsageError("Pass either --online or --offline, not both")
    if male and female:
        raise click.UsageError("Pass either --male or --female, not both")

    if not male and not female:
        console.print("[red]Skipping TTS configuration, pass '--male' or '--female' to set language defaults[/red]")

    try:
        from ovos_utils.lang import standardize_lang_tag
        stdlang = standardize_lang_tag(lang, macro=True)
        console.print(f"[blue]Standardized lang-code:[/blue] {stdlang}")
    except ImportError:
        stdlang = lang
        console.print(f"[red]ERROR: Failed to standardize lang tag, please install latest 'ovos-utils' package[/red]")

    config = LocalConf(USER_CONFIG)
    config["tts"] = {"ovos-tts-plugin-server": {}}
    config["stt"] = {"ovos-stt-plugin-server": {}}

    def do_merge(folder):
        l2 = stdlang.split("-")[0]
        recs_path = f"{os.path.dirname(__file__)}/recommends"
        path = f"{recs_path}/{folder}/{lang.lower()}.conf"
        if not os.path.isfile(path):
            paths = [f"{recs_path}/{folder}/{f}"
                     for f in os.listdir(f"{recs_path}/{folder}") if f.startswith(l2)]
            if paths:
                path = paths[0]

        if not os.path.isfile(path):
            console.print(f"[red]ERROR: {folder} not available for {stdlang}[/red]")
            return

        c = LocalConf(path)
        config.merge(c)
        console.print(f"Merged config: {c.path}")

    do_merge("base")
    if offline:
        do_merge("offline_stt")
        if male:
            do_merge("offline_male")
        elif female:
            do_merge("offline_female")

    elif online:
        config["tts"]["module"] = "ovos-tts-plugin-server"
        config["stt"]["module"] = "ovos-stt-plugin-server"
        do_merge("online_stt")
        if male:
            do_merge("online_male")
        elif female:
            do_merge("online_female")

    config["lang"] = stdlang

    try:
        from ovos_plugin_manager.stt import find_stt_plugins
        from ovos_plugin_manager.tts import find_tts_plugins

        available_stt = list(find_stt_plugins().keys())
        available_tts = list(find_tts_plugins().keys())

        console.print("[blue]Available STT plugins:[/blue]")
        for plugin in available_stt:
            console.print(f"  - '{plugin}'")
        console.print("[blue]Available TTS plugins:[/blue]")
        for plugin in available_tts:
            console.print(f"  - '{plugin}'")

        missing_plugins = []
        if config["stt"]["module"] not in available_stt:
            missing_plugins.append(f"STT plugin '{config['stt']['module']}'")
        if config["tts"]["module"] not in available_tts:
            missing_plugins.append(f"TTS plugin '{config['tts']['module']}'")

        if missing_plugins:
            console.print("[yellow]WARNING: The following plugins are missing:[/yellow]")
            for plugin in missing_plugins:
                console.print(f"  - {plugin}")
            console.print("Please install the missing plugins using 'pip install <plugin_name>'")
    except ImportError:
        console.print("[yellow]WARNING: 'ovos-plugin-manager' not installed. Skipping plugin validation.[/yellow]")
        console.print(
            "To enable plugin validation, install 'ovos-plugin-manager' using 'pip install ovos-plugin-manager'")

    config.store()
    console.print(f"Config updated: {config.path}")

    print_json(json.dumps({k: v for k, v in config.items()
                           if k in ["lang",
                                    "tts", "stt",
                                    "system_unit",
                                    "temperature_unit",
                                    "windspeed_unit",
                                    "precipitation_unit",
                                    "date_format",
                                    "time_format",
                                    "spoken_time_format"]}))


@config.command()
@click.option("--user", "-u", is_flag=True, help="User Configuration")
@click.option("--system", "-s", is_flag=True, help="System Configuration")
@click.option("--remote", "-r", is_flag=True, help="Remote Configuration")
@click.option("--section", default="", show_default=False,
              help="Choose a specific section from the underlying configuration")
@click.option("--list-sections", "-l", is_flag=True, help="List the sections based on the underlying configuration")
def show(user, system, remote, section, list_sections):
    """\b
    By ommiting a specific configuration a joined configuration table is shown. (which is the one ultimately gets loaded by ovos)
    \b
    Based on this consideration you can further trim the table by section.
    If the sections are unknown you may want to list them.
    \b
    Examples: 
    ovos-config show                                    # shows all the configuration values in a table format
    ovos-config show -s -l                              # shows the sections of the system configuration
    ovos-config show -u --section base                  # shows only the base (ie. top level) values of the user configuration 

    note: joining pattern: user > system > remote > default
    \b
    """
    if not any([user, system, remote]):
        name, config = CONFIGS[0]
    elif system:
        name, config = CONFIGS[1]
    elif user:
        name, config = CONFIGS[2]
    elif remote:
        name, config = CONFIGS[3]

    # based on chosen configuration
    if name != "Joined":
        _sections = [k for k, v in config.items() if isinstance(v, dict)]
        if [k for k, v in config.items() if not isinstance(v, dict)]:
            _sections.append("base")
    else:
        _sections = SECTIONS

    if list_sections:
        console.print(f"Available sections ({name} config): " + " ".join(_sections))
        exit()

    if section:
        # general info that no such key exists
        if section not in SECTIONS:
            console.print(f"The section `{section}` doesn't exist. Please chose"
                          f" from {' '.join(SECTIONS)}")
            exit()
        # based on chosen configuration
        elif section not in _sections:
            found_in = [f"`{_name}`" for _name, _config in CONFIGS
                        if section in _config and _name != name]
            console.print(f"The section `{section}` doesn't exist in the {name} "
                          f"Configuration. It is part of the {'/'.join(found_in)} "
                          "Configuration though")
            exit()
        elif section == "base":
            _config = {k: v for k, v in config.items() if not isinstance(v, dict)}
        else:
            _config = config[section]
    else:
        # sorted dict based on depth
        _config = {key: value for key, value in
                   sorted(config.items(), key=lambda item: dictDepth(item[1]))}

    section_info = f", Section: {section}" if section else ""
    additional_info = f"(Configuration: {name}{section_info})"

    table = Table(show_header=True, header_style="bold red")
    table.add_column(f"Configuration keys {additional_info}", min_width=60)
    table.add_column("Value", min_width=20)

    drawTable(_config, table)
    console.print(table)


@config.command()
@click.option("--key", "-k", required=True, help="the key (or parts thereof) which should be searched")
def get(key):
    """\b
    Search for config keys in the (joined) configuration
    \b
    Meant to either loosely search for keys resp. parts thereof or specific dictionary paths (form: `/path/to/key`)
    The loose search will output a list of found keys - if there are multiple - that match the query (full or in part)
    The strict search performs a query to a specific path and will only output the value. (usefull for shell scripting)
    \b
    Examples: 
    ovos-config get -k lang                              # get all lang key values across the configuration
    ovos-config get -k /tts/module                       # get the key at the position specified
    """
    strict = True if "/" in key else False
    if strict:
        if not key.startswith("/"):
            console.print("A strict key search has to start with `/` (root)")
            exit()

        value = pathGet(CONFIG, key)
        # Configuration is excepting ValueError itself
        if value is None:
            exit()

        console.print(f"[red]{value}[/red]")
    else:
        values = list(walkDict(CONFIG, key))
        if not values:
            console.print(f"No key with the name {key} found")
        else:
            for path, value in values:
                console.print((f"Value: [red]{value}[/red], "
                               f"found in [red]/{'/'.join(path)}[/red]"))


@config.command()
@click.option("--key", "-k", required=True, help="the key (or parts thereof) which should be searched")
@click.option("--value", "-v", help="value the key should get associated with")
def set(key, value):
    """\b
    Sets a config key in the user configuration
    \b
    Loosely searches a config key and if multiple are found asks which key and value should be written.
    The user may pass a value to bypass prompting.
    \b
    Examples: 
    ovos-config set -k gui                              # lists all config keys containing "gui" (either as endpoint or in path),
                                                        # let the user choose the specific key and asks for the value
    ovos-config set -k blacklisted_skills -v myskill    # Adds "myskill" as an blacklisted skill
                                                        # Since this is a pretty specific key and a value is passed, the user won't be prompted
    """
    key = key.lstrip("/")
    tuples = list(walkDict(CONFIG, key, full_path=True))
    values = [tup[1] for tup in tuples]
    paths = ["/".join(tup[0]) for tup in tuples]

    if len(paths) > 1:
        table = Table(show_header=True, header_style="bold red")
        table.add_column("#")
        table.add_column("Path", min_width=20)
        table.add_column("Value")

        for i, path in enumerate(paths):
            table.add_row(str(i), path, str(values[i]))
        console.print(table)

        exit_ = str(len(paths))
        choice = Prompt.ask(f"Which value should be changed? ({exit_}='Exit')",
                            choices=[str(i) for i in range(0, len(paths) + 1)])
        if choice == exit_:
            console.print("User exit", style="red")
            exit()
    elif not paths:
        console.print("[red]Error:[/red] No key that fits the query")
        exit()
    else:
        choice = 0

    selected_path = paths[int(choice)]
    selected_value = values[int(choice)]
    selected_type = selected_value.__class__.__name__
    # to not irritate the use to suggest typing `["xyz"]`
    if selected_type == "list":
        selected_type = "str"

    if not value:
        value = Prompt.ask(("Please enter the value to be stored "
                            f"(type: [red]{selected_type}[/red]) "))
        value = value.replace('"', '').replace("'", "").replace("`", "")

    local_conf = CONFIGS[2][1]
    _value = None
    # type checking/casting
    try:
        if isinstance(selected_value, str):
            _value = value
        elif isinstance(selected_value, bool):
            if value in ["true", "True", "1", "on"]:
                _value = True
            elif value in ["false", "False", "0", "off"]:
                _value = False
            else:
                raise TypeError
        elif isinstance(selected_value, list):
            try:
                _value = pathGet(local_conf, selected_path)
            except KeyError:
                _value = list()
                console.print(("Note: defining lists in the user config "
                               "will override subsequent list configurations"),
                              style="grey53")
            _value.append(value)
        elif isinstance(selected_value, int):
            _value = int(value)
        elif isinstance(selected_value, float):
            _value = float(value)
    except (TypeError, ValueError):
        console.print(f"[red]Error:[/red] The value passed can't be cast into {selected_type}")
        exit()

    pathSet(local_conf, selected_path, _value)
    local_conf.store()


if __name__ == "__main__":
    config()
