from .registry_editor import *

def create_command(key_path: str, key_name: str, command: str):
    """
    Creates a command in the context menu.

    :param key_path: The path of the parent key in the Windows Registry.
    :type key_path: str
    :param key_name: The name of the command.
    :type key_name: str
    :param command: The command to execute.
    :type command: str
    """
    hive = get_hive_from_key_path(key_path)

    command_key_path = f"{key_path}\\{key_name}"
    create_registry_key(key_path, key_name, hive)
    create_registry_key(command_key_path, "command", hive)
    set_default_value(f"{command_key_path}\\command", command, hive)

def create_cascading_menu(parent_key_path: str, menu_name: str):
    """
    Creates a cascading menu in the context menu.

    :param parent_key_path: The path of the parent key in the Windows Registry.
    :type parent_key_path: str
    :param menu_name: The name of the cascading menu.
    :type menu_name: str
    """
    hive = get_hive_from_key_path(parent_key_path)

    menu_key_path = f"{parent_key_path}\\{menu_name}"
    create_registry_key(parent_key_path, menu_name, hive)
    set_default_value(menu_key_path, "", hive)
    create_string_value(menu_key_path, "MUIVerb", menu_name, hive)
    create_string_value(menu_key_path, "subcommands", "", hive)
    
    shell_key_path = f"{menu_key_path}\\shell"
    create_registry_key(shell_key_path, "", hive)
    
    return shell_key_path

def add_command_to_cascading_menu(shell_key_path: str, key_name: str, command: str):
    """
    Adds a command to a cascading menu in the context menu.

    :param shell_key_path: The path of the shell key in the Windows Registry.
    :type shell_key_path: str
    :param key_name: The name of the command.
    :type key_name: str
    :param command: The command to execute.
    :type command: str
    """
    create_command(shell_key_path, key_name, command)

def add_icon(key_path: str, icon_path: str):
    """
    Adds an icon to a key in the Windows Registry.

    :param key_path: The path of the key in the Windows Registry.
    :type key_path: str
    :param icon_path: The path of the icon to add.
    :type icon_path: str
    """
    create_string_value(key_path, "Icon", icon_path)

def get_scopes(scope: str):
    """
    Gets the scopes of the context menu.
    
    :param scope: The scope of the context menu.
    :type scope: str
    :return: The scopes of the context menu.
    :rtype: list
    :raises ValueError: If the scope is invalid.
    """
    
    if scope == "FILES":
        key_path = "Software\\Classes\\*\\shell"
    elif scope == "DIRECTORY":
        key_path = "Software\\Classes\\Directory\\Background\\shell"
    elif scope == "DIRECTORY_BACKGROUND":
        key_path = "Software\\Classes\\Directory\\Background\\shell"
    elif scope == "DRIVE":
        key_path = "Software\\Classes\\Drive\\shell"
    elif scope.startswith("EXTENSION_SFA"):
        extension = scope.split("_")[2]
        key_path = f"Software\\Classes\\SystemFileAssociations\\{extension}\\shell"
    else:
        raise ValueError("Invalid scope.")
    
    return key_path

def transform_path(path: str) -> str:
    """
    Transform a path of the form /Abuelo/Hijo/Nieto/ to /Abuelo/shell/Hijo/shell/Nieto/shell
    
    :param path: The path to transform.
    :type path: str
    :return: The transformed path.
    :rtype: str
    """
    path = path.strip("/")
    parts = path.split("/")
    transformed = [parts[0], "shell"]
    for part in parts[1:]:
        transformed += [part, "shell"]
    return "/" + "/".join(transformed) + "/"

def key_exists(key_path: str) -> bool:
    """
    Checks if a key exists in the Windows Registry.

    :param key_path: The path of the key in the Windows Registry.
    :type key_path: str
    :return: True if the key exists, False otherwise.
    :rtype: bool
    """
    
    hive = get_hive_from_key_path(key_path)
    parent_key_path, key_name = key_path.rsplit("\\", 1)
    
    return key_name in list_keys(parent_key_path, hive)