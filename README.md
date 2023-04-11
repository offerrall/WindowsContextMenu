# Context Menu Manager

Context Menu Manager is a Python library for creating and managing context menu items in Windows.

This library provides a simple and intuitive API for creating context menu items for files and folders in Windows. It supports creating simple commands and nested menus, as well as listing and removing existing items.

This library was created for personal use but is shared in the hopes that it may be useful to others or inspire contributions. Contributions are welcome via pull requests.

## Installation

This library not requires any dependencies, simply download the source code and import the `WindowsContextMenu` module.

## Main Features
- `Create commands`: Add custom commands to the context menu for files and directories.
- `Create folders`: Organize your custom commands by creating nested folders in the context menu.
- `Remove items`: Remove custom commands and folders from the context menu.
- `Check existence`: Check if a command or folder already exists in the context menu.
- `Get command`: Get the command associated with a specific item in the context menu.
- `List items`: List all folders and commands in the context menu.
- `Determine item type`: Check if an item in the context menu is a folder or a command.
- `Get available scopes`: List all available scopes for the context menu, such as "FILES" and "DIRECTORY".

## Usage

All Examples and API documentation can be found in the [Doc](test).

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

