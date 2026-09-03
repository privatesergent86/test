import os
import shutil

# Folder to search
source_folder = "C:/Users/David/Documents"
destination_folder = "C:/Users/David/Documents/Python_Projects"

# Create destination folder if it doesn't exist
os.makedirs(destination_folder, exist_ok=True)

# Walk through all subfolders
for root, dirs, files in os.walk(source_folder):
    for file in files:
        if file.endswith(".py"):
            source_path = os.path.join(root, file)
            destination_path = os.path.join(destination_folder, file)
            shutil.move(source_path, destination_path)
            print(f"Moved: {file}")
