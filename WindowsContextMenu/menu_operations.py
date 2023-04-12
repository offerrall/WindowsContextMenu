from .utils import *
from .registry_editor import get_hive_from_key_path, get_command_from_item

def list_items(scope: str, parent: str = None) -> list:
    """
    Lists all the items (folders and commands) in the context menu for a specific scope or under a specific folder.

    :param scope: The scope of the context menu.
    :type scope: str
    :param parent: The name of the parent key, none is the root.
    :type parent: str, optional
    :return: A list of the item names.
    :rtype: list
    """

    key_path = get_scopes(scope)
    if parent:
        key_path = key_path + transform_path(parent).replace("/", "\\")
    else:
        key_path = key_path + "\\"

    items = list_keys(key_path)
    return items

def mkdir_menu_context(scope: str, key_name: str, icon: str = None, parent: str = None) -> str:
    """ Creates a folder in the menu context.
    
    :param scope: The scope of the context menu.
    :type scope: str
    :param key_name: The name of the folder.
    :type key_name: str
    :param icon: The path of the icon to add.
    :type icon: str
    :param parent: The name of the parent key. None is the root.
    :type parent: str
    :return: The path of the folder in the registry.
    :rtype: str
    """
    
    key_path = get_scopes(scope)
    if parent:
        key_path = key_path + transform_path(parent).replace("/", "\\")
    else:
        key_path = key_path + "\\"
    
    
    
    create_cascading_menu(key_path, key_name)
    if icon:
        add_icon(f"{key_path}\\{key_name}", icon)
    
    return f"{key_path}{key_name}\\shell"

def create_simple_command(scope: str, key_name: str, command: str, icon: str = None, parent: str = None) -> str:
    """
    Creates a simple command in the context menu with an optional icon.

    :param scope: The scope of the context menu.
    :type scope: str
    :param key_name: The name of the command, %1 will be replaced by the path of the file.
    :type key_name: str
    :param command: The command to execute.
    :type command: str
    :param icon: The path of the icon to add, if any.
    :type icon: str, optional
    :param parent: The name of the parent key, none is the root.
    :type parent: str, optional
    :return: The path of the command in the registry.
    :rtype: str
    """
    
    key_path = get_scopes(scope)
    if parent:
        key_path = key_path + transform_path(parent).replace("/", "\\")
    else:
        key_path = key_path + "\\"

    create_command(key_path, key_name, command)
    if icon:
        add_icon(f"{key_path}\\{key_name}", icon)

    return f"{key_path}{key_name}\\command"

def remove_item(scope: str, key_name: str, parent: str = None):
    """
    Removes a folder or a command from the context menu.

    :param scope: The scope of the context menu.
    :type scope: str
    :param key_name: The name of the folder or command to remove.
    :type key_name: str
    :param parent: The name of the parent key, none is the root.
    :type parent: str, optional
    """

    hive  = get_hive_from_key_path(get_scopes(scope))
    
    key_path = get_scopes(scope)
    if parent:
        key_path = key_path + transform_path(parent).replace("/", "\\")
    else:
        key_path = key_path + "\\"

    delete_key(f"{key_path}\\{key_name}", hive)

def item_exists(scope: str, key_name: str, parent: str = None) -> bool:
    """
    Checks if an item (folder or command) exists in the context menu for a specific scope or under a specific folder.

    :param scope: The scope of the context menu.
    :type scope: str
    :param key_name: The name of the item (folder or command) to check for.
    :type key_name: str
    :param parent: The name of the parent key, none is the root.
    :type parent: str, optional
    :return: True if the item exists, False otherwise.
    :rtype: bool
    """

    key_path = get_scopes(scope)
    if parent:
        key_path = key_path + transform_path(parent).replace("/", "\\")
    else:
        key_path = key_path + "\\"

    return key_exists(f"{key_path}\\{key_name}")

def get_item_command(scope: str, key_name: str, parent: str = None) -> str:
    """
    Gets the command associated with a context menu item for a specific scope or under a specific folder.

    :param scope: The scope of the context menu.
    :type scope: str
    :param key_name: The name of the item (folder or command) to get the command for.
    :type key_name: str
    :param parent: The name of the parent key, none is the root.
    :type parent: str, optional
    :return: The command associated with the context menu item, or an empty string if the item has no command.
    :rtype: str
    """

    key_path = get_scopes(scope)
    if parent:
        key_path = key_path + transform_path(parent).replace("/", "\\")
    else:
        key_path = key_path + "\\"

    item_key_path = f"{key_path}\\{key_name}"
    command = get_command_from_item(item_key_path)
    return command

def item_type(scope: str, key_name: str, parent: str = None) -> str:
    """
    Determines if an item in the context menu is a folder or a command.

    :param scope: The scope of the context menu.
    :type scope: str
    :param key_name: The name of the item (folder or command) to check for.
    :type key_name: str
    :param parent: The name of the parent key, none is the root.
    :type parent: str, optional
    :return: The type of the item, either 'folder' or 'command'.
    :rtype: str
    :raises ValueError: If the item is not found.
    """

    key_path = get_scopes(scope)
    if parent:
        key_path = key_path + transform_path(parent).replace("/", "\\")
    else:
        key_path = key_path + "\\"

    full_key_path = f"{key_path}\\{key_name}"

    # Check if the item has a "command" subkey
    if "command" in list_keys(full_key_path):
        return "command"
    # Check if the item has a "shell" subkey
    elif "shell" in list_keys(full_key_path):
        return "folder"
    else:
        raise ValueError("Item not found.")

def get_available_scopes():
    """
    Gets the available scopes for the context menu.

    FILES: Applies to all files
    DIRECTORY: Applies to directories/folders
    DIRECTORY_BACKGROUND: Applies to directory/folder backgrounds
    DRIVE: Applies to drives (e.g., USB drives)
    EXTENSION_SFA_: System File Association (SFA)
    applies to files with a specific extension. The extension is specified -> EXTENSION_SFA_<extension>
    
    Example:
        create_simple_command("EXTENSION_SFA_.jpg", "cmd", "cmd.exe")
    
    :return: A dictionary containing the available scopes and their descriptions.
    :rtype: dict
    """
    available_scopes = {
        "FILES": "Applies to all files",
        "DIRECTORY": "Applies to directories/folders",
        "DIRECTORY_BACKGROUND": "Applies to directory/folder backgrounds",
        "DRIVE": "Applies to drives (e.g., USB drives)",
        "EXTENSION_SFA_": "Applies to files with a specific extension. Look at the documentation for more information.",
        "RECYCLE_BIN": "Applies to the recycle bin",
        "DESKTOP": "Applies to the desktop",
    }

    return available_scopes
