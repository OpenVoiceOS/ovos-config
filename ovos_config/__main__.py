#!/bin/env python3
from typing import Any, Tuple

import rich_click as click
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
        s = f'{key:>{4*level+len(key)}}'
        if not isinstance(value, dict):
            table.add_row(s, str(value))
        else:
            if level == 0:
                table.add_section()
            table.add_row(f'[red]{s}[/red]')
            drawTable(value, table, level+1)
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
                yield path+(k,), dic[k]
                found = False

        # endpoint
        if type(dic[k]) != dict:
            if found:
                yield path+(k,), dic[k]
        else:
            yield from walkDict(dic[k],
                                key,
                                full_path,
                                path+(k,),
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
@click.option("--user", "-u", is_flag=True, help="User Configuration")
@click.option("--system", "-s", is_flag=True, help="System Configuration")
@click.option("--remote", "-r", is_flag=True, help="Remote Configuration")
@click.option("--section", default="", show_default=False, help="Choose a specific section from the underlying configuration")
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
        if len([k for k, v in config.items() if not isinstance(v, dict)]):
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
    Loosly searches a config key and if multiple are found asks which key and value should be written.
    The user may pass a value to bypass prompting.
    \b
    Examples: 
    ovos-config set -k gui                              # lists all config keys containing "gui" (either as endpoint or in path),
                                                        # let the user choose the specific key and asks for the value
    ovos-config set -k blacklisted_skills -v myskill    # Adds "myskill" as an blacklisted skill
                                                        # Since this is a pretty specific key and a value is passed, the user won't be prompted
    """
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
                            choices=[str(i) for i in range(0, len(paths)+1)])
        if choice == exit_:
            console.print("User exit", style="red")
            exit()
    elif not paths:
        console.print(f"[red]Error:[/red] No key that fits the query")
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
        value = value.replace('"','').replace("'","").replace("`","")

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
    
    local_conf = CONFIGS[2][1]
    pathSet(local_conf, selected_path, _value)
    local_conf.store()

if __name__ == "__main__":
    config()
