import winreg

def get_hive_from_key_path(key_path: str) -> int:
    """
    Gets the appropriate hive based on the key path.

    :param key_path: The path of the key in the Windows Registry.
    :type key_path: str
    :return: The hive to be used (HKEY_LOCAL_MACHINE or HKEY_CURRENT_USER).
    :rtype: int
    """
    if "SystemFileAssociations" in key_path:
        return winreg.HKEY_LOCAL_MACHINE
    else:
        return winreg.HKEY_CURRENT_USER

def create_registry_key(key_path: str, key_name: str, hive = winreg.HKEY_CURRENT_USER):
    """
    Creates a key in the Windows Registry.

    :param key_path: The path of the key in the Windows Registry.
    :type key_path: str
    :param key_name: The name of the key to create.
    :type key_name: str
    :raises WindowsError: If the key cannot be created in the Windows Registry.
    """
    try:
        key = winreg.CreateKeyEx(
            hive, key_path, 0, winreg.KEY_ALL_ACCESS
        )
        winreg.CreateKeyEx(key, key_name, 0, winreg.KEY_ALL_ACCESS)
        winreg.CloseKey(key)
    except WindowsError as e:
        raise WindowsError(f"Error creating key '{key_name}' in '{key_path}': {str(e)}")

def set_default_value(key_path: str, value: str, hive = winreg.HKEY_CURRENT_USER):
    """
    Sets the default value of a key in the Windows Registry.

    :param key_path: The path of the key in the Windows Registry.
    :type key_path: str
    :param value: The value to set as the default value.
    :type value: str
    :raises WindowsError: If the default value cannot be set in the Windows Registry.
    """
    try:
        key = winreg.CreateKeyEx(
            hive, key_path, 0, winreg.KEY_SET_VALUE
        )
        winreg.SetValueEx(key, "", 0, winreg.REG_SZ, value)
        winreg.CloseKey(key)
    except WindowsError as e:
        raise WindowsError(f"Error setting default value for key '{key_path}': {str(e)}")

def create_string_value(key_path: str, value_name: str, value: str, hive = winreg.HKEY_CURRENT_USER):
    """
    Creates a string value in the Windows Registry.

    :param key_path: The path of the key in the Windows Registry.
    :type key_path: str
    :param value_name: The name of the string value to create.
    :type value_name: str
    :param value: The value to set.
    :type value: str
    :raises WindowsError: If the string value cannot be created in the Windows Registry.
    """
    try:
        key = winreg.CreateKeyEx(
            hive, key_path, 0, winreg.KEY_SET_VALUE
        )
        winreg.SetValueEx(key, value_name, 0, winreg.REG_SZ, value)
        winreg.CloseKey(key)
    except WindowsError as e:
        raise WindowsError(f"Error creating string value '{value_name}' in '{key_path}': {str(e)}")

def list_keys(path: str, hive = winreg.HKEY_CURRENT_USER):
    """
    Lists all the subkeys at the given path in the specified hive.

    :param path: The path of the key in the Windows Registry.
    :type path: str
    :param hive: The hive of the Windows Registry to list the subkeys from. Default is HKEY_CURRENT_USER.
    :type hive: HKEY (Optional)
    :return: A list of subkeys.
    :rtype: list
    """
    open_key = winreg.OpenKey(hive, path)
    key_amt = winreg.QueryInfoKey(open_key)[0]
    keys = []

    for count in range(key_amt):
        subkey = winreg.EnumKey(open_key, count)
        keys.append(subkey)

    return keys

def get_command_from_item(item_key_path: str) -> str:
    """
    Gets the command from an item in the context menu.

    :param item_key_path: The path of the item key in the Windows Registry.
    :type item_key_path: str
    :return: The command associated with the context menu item, or an empty string if the item has no command.
    :rtype: str
    """

    command_key_path = f"{item_key_path}\\command"
    hive = get_hive_from_key_path(item_key_path)

    try:
        open_key = winreg.OpenKey(hive, command_key_path)
        command_value, _ = winreg.QueryValueEx(open_key, "")
        winreg.CloseKey(open_key)
        return command_value
    except WindowsError:
        raise WindowsError(f"The key '{command_key_path}' does not exist.")

def delete_key(path: str, hive = winreg.HKEY_CURRENT_USER):
    """
    Deletes the desired key and all other subkeys at the given path in the specified hive.

    :param path: The path of the key in the Windows Registry.
    :type path: str
    :param hive: The hive of the Windows Registry to delete the key from. Default is HKEY_CURRENT_USER.
    :type hive: HKEY (Optional)
    :raises WindowsError: If the key cannot be deleted in the Windows Registry.
    """
    
    open_key = winreg.OpenKey(hive, path, 0, winreg.KEY_ALL_ACCESS)
    subkeys = list_keys(path, hive)

    if len(subkeys) > 0:
        for key in subkeys:
            delete_key(path + '\\' + key, hive)
    winreg.DeleteKey(open_key, "")