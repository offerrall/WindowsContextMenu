# WindowsContextMenu

WindowsContextMenu is a Python library for creating and managing context menu items in Windows.

This library provides a simple and intuitive API for creating context menu items for files and folders in Windows. It supports creating simple commands and nested menus, as well as listing and removing existing items.

This library was created for personal use but is shared in the hopes that it may be useful to others or inspire contributions. Contributions are welcome via pull requests or issues.

## Installation

Use pip to install the library. The library does not require additional dependencies.

```bash
pip install WindowsContextMenu
```

## Main Features
- `Create commands`: This feature allows you to add custom commands to the context menu for files and directories.
- `Create folders`: This feature enables you to organize your custom commands by creating nested folders in the context menu.
- `Remove items`: Remove custom commands and folders from the context menu.
- `Check existence`: Check if a command or folder already exists in the context menu.
- `Get command`: Get the command associated with a specific item in the context menu.
- `List items`: List all folders and commands in the context menu.
- `Determine item type`: Check if an item in the context menu is a folder or a command.
- `Get available scopes`: List all available scopes for the context menu, such as "FILES" and "DIRECTORY".

## Windows Versions

This library is compatible with Windows 7, 8, 8.1 and 10.
Windows 11 is compatible if remove the new w11 menu context.

## Scopes

In Windows, a context menu can have different scopes depending on where it is displayed. The available scopes are:

- `FILES`: for context menus displayed when right-clicking on a file.
- `DIRECTORY`: for context menus displayed when right-clicking on a folder.
- `DIRECTORY_BACKGROUND`: for context menus displayed when right-clicking on the background of a folder.
- `DRIVE`: for context menus displayed when right-clicking on a drive.
- `EXTENSION_SFA_<extension>`: for context menus displayed when right-clicking on a file with a specific extension.
- `RECYCLE_BIN`: for context menus displayed when right-clicking on the Recycle Bin.
- `DESKTOP`: for context menus displayed when right-clicking on the desktop.

Paths in the registry for the different scopes:
- `FILES`: `HKEY_CURRENT_USER\*\shell`
- `DIRECTORY`: `HKEY_CURRENT_USER\Software\Classes\Directory\Background\shell`
- `DIRECTORY_BACKGROUND`: `HKEY_CURRENT_USER\Software\Classes\Directory\Background\shell`
- `DRIVE`: `HKEY_CURRENT_USER\Software\Classes\Drive\shell`
- `EXTENSION_SFA_<extension>`: `HKEY_LOCAL_MACHINE\Software\Classes\SystemFileAssociations\{extension}\shell`
- `RECYCLE_BIN`: `HKEY_CLASSES_ROOT\CLSID\{645FF040-5081-101B-9F08-00AA002F954E}\shell`
- `DESKTOP`: `HKEY_CLASSES_ROOT\DesktopBackground\Shell\`	

The `get_available_scopes()` function can be used to get a list of all available scopes. The scope parameter is used in various functions to specify where the context menu items should be created or removed.

## Usage

All Examples and API documentation can be found in the [Doc](https://offerrall.github.io/WindowsContextMenu/WindowsContextMenu.html).
Little example:

```python

from WindowsContextMenu.menu_operations import create_simple_command, mkdir_menu_context, get_available_scopes

# List all available scopes for the context menu
scopes = get_available_scopes()

# Create a simple command in the context menu for all files
create_simple_command("FILES", "Open with Notepad", "notepad.exe %1")

# Create a simple command in the context menu for directories
create_simple_command("DIRECTORY", "Open Command Prompt Here", "cmd.exe /k cd %1")

# Create a folder in the context menu for all files
mkdir_menu_context("FILES", "My Custom Commands")

# Create a command inside the previously created folder
create_simple_command("FILES", "Custom Command 1", "cmd.exe /k echo Custom Command 1", parent="My Custom Commands")

# Create a Folder inside the previously created folder
mkdir_menu_context("FILES", "My Subfolder", parent="My Custom Commands")

# Create a command inside the previously created subfolder
create_simple_command("FILES", "Custom Command 2", "cmd.exe /k echo Custom Command 2", parent="My Custom Commands/My Subfolder")

```

Considerations:

- The icons must be in .ico format and should not be deleted once created. For instance, if you create an icon named `my_icon.ico`, make sure to keep this file in the same location and do not delete it.
- The parent folder path must be absolute and in Linux format, /FFmpeg/Video/Mp4/ToMp3. This means that if you are creating a nested folder or command, the path should look like `/ParentFolder/ChildFolder`, and not like `ParentFolder\ChildFolder`.
- The parent folder must exist in order to create the child folder. For example, if you want to create a folder named `ChildFolder` inside `ParentFolder`, `ParentFolder` must already exist.
- Use %1 in the command to get the path of the selected file or folder, for example: "notepad.exe %1". This means that if you create a command like `"notepad.exe %1"`, the `%1` will be replaced by the path of the file or folder that you right-clicked on.
- All functions raise an exception if an error occurs of type `WindowsError`. This means that if an error occurs during the execution of a command, the function will stop and raise a `WindowsError`, which you can catch and handle in your code.


## TODO
- Add support for other scopes.
  - New Menu
  - Send To
  - Open With
  - win+X

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
