# create_list_dirs.py

import os

# Create directories
os.makedirs("test_dir/sub_dir", exist_ok=True)

print("Directories created.")

# Current directory
print("Current directory:", os.getcwd())

# List files
files = os.listdir(".")
print("\nFiles in current directory:")

for f in files:
    print(f)