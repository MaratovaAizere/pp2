# copy_delete_files.py

import shutil
import os

source = "sample.txt"
backup = "sample_backup.txt"

# Copy file
shutil.copy(source, backup)
print("File copied to backup.")

# Delete backup safely
if os.path.exists(backup):
    os.remove(backup)
    print("Backup file deleted.")
else:
    print("Backup file not found.")