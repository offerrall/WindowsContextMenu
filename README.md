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

## Special Variables in Windows Context Menu

In the context of Windows context menus, certain special variables, also known as "command argument variables", can be used to refer to different paths and items. Here, we will explain some of the most commonly used ones:

### `%1` or `%L`

These variables refer to the full path of the file or folder that you have right-clicked on. When you create a command like `"notepad.exe %1"`, the `%1` will be replaced by the path of the file or folder that you right-clicked on.

### `%V`

This variable refers to the selected item's folder path. It is most often used in conjunction with the `DIRECTORY_BACKGROUND` scope, where the right-click does not happen on a specific file or folder but in the background of a directory.

### `%W`

This variable is used to get the working directory when the command is executed.

### `SystemFolder`

This variable can be used to refer to system folders such as "Desktop", "My Documents", "Program Files", etc.

### `AppData`

This variable can be used to refer to the current user's AppData folder.

### `ProgramFiles`

This variable can be used to refer to the Program Files directory.

Note: These variables can be combined to refer to more complex paths. For example, `"%SystemFolder%\My Documents"` refers to the My Documents folder in the system folder.



## Considerations for using WindowsContextMenu

When using the WindowsContextMenu library, there are some important considerations to keep in mind:

1. **Icon format**: The icons used for the context menu items must be in `.ico` format. Additionally, once the icon is assigned, it should not be deleted or moved from its original location. For instance, if you have an icon named `my_icon.ico`, it should persist in its current path even after its use.

2. **Path formatting**: Paths used in the library, especially for specifying parent and child folders, must follow the Unix (or Linux) path format, i.e., `/ParentFolder/ChildFolder`. The use of backslashes `\` common in Windows paths is not accepted.

3. **Pre-existing parent folder**: Before you can create a child folder under a parent folder, the parent folder must already exist in the context menu. If you want to create a folder named `ChildFolder` inside `ParentFolder`, `ParentFolder` should already be present in your context menu.


4. **Error handling**: The library functions are designed to throw a `WindowsError` exception when any error occurs during their execution. These exceptions can be caught and handled in your code to manage errors and provide appropriate feedback.

Remember, understanding and following these considerations can help you avoid common mistakes and make the most of the WindowsContextMenu library.


## TODO
- Add support for other scopes.
  - New Menu
  - Send To
  - Open With
  - win+X

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
