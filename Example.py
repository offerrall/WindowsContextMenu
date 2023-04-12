from WindowsContextMenu.menu_operations import *


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

# List all items (folders and commands) in the context menu for all files
print(list_items("FILES"))

# Check if an item exists in the context menu
print(item_exists("FILES", "Open with Notepad"))

# Get the command associated with a context menu item
print(get_item_command("FILES", "Open with Notepad"))

# Determine the type of a context menu item (folder or command)
print(item_type("FILES", "My Custom Commands"))

# Remove a command from the context menu
remove_item("FILES", "Custom Command 1", parent="My Custom Commands")

# Remove a folder from the context menu
remove_item("FILES", "My Custom Commands")

# Create a top-level folder in the context menu for all files
mkdir_menu_context("FILES", "My Commands")

# Create a nested folder inside the top-level folder
mkdir_menu_context("FILES", "Subfolder", parent="My Commands")

# Create a command inside the nested folder
create_simple_command("FILES", "Subfolder Command", "cmd.exe /k echo Subfolder Command", parent="My Commands/Subfolder")

# List all items in the top-level folder
print(list_items("FILES", parent="My Commands"))

# List all items in the nested folder
print(list_items("FILES", parent="My Commands/Subfolder"))

# Delete the top-level folder and all its contents
remove_item("FILES", "My Commands")

# Create a command in the Desktop context menu
create_simple_command("DESKTOP", "Escritorio", "cmd.exe /k cd %1")

# Create a command in the Recycle Bin context menu
create_simple_command("RECYCLE_BIN", "Recycle Bin Custom", "cmd.exe")