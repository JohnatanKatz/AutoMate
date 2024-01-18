import shutil
import os
import subprocess

# Get the current directory where this script is running
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define the relative path to the main.spec file
spec_file_path = os.path.join(current_dir, 'main.spec')

# Define the PyInstaller command using the relative path
pyinstaller_command = f"pyinstaller {spec_file_path} -y"

# Run the PyInstaller command
print(pyinstaller_command)
subprocess.run(pyinstaller_command, shell=True, check=True)

# Define the source and destination paths relative to the current directory
# Adjust these paths as needed based on your project structure
source_path = os.path.join(current_dir, 'dist', 'AutoMate', '_internal', 'assets')
destination_path = os.path.join(current_dir, 'dist', 'AutoMate', 'assets')

print("source_path", source_path, "\ndestination", destination_path, "\ncurrent_dir", current_dir)

# Check if the destination path exists and remove it if it does

if os.path.exists(destination_path):
    shutil.rmtree(destination_path)

# Move the assets folder from the source to the destination
shutil.move(source_path, destination_path)
