# read_files.py

file_path = "sample.txt"

# read()
with open(file_path, "r") as f:
    content = f.read()
    print("Using read():")
    print(content)

# readline()
with open(file_path, "r") as f:
    print("\nUsing readline():")
    print(f.readline())

# readlines()
with open(file_path, "r") as f:
    print("\nUsing readlines():")
    lines = f.readlines()
    for line in lines:
        print(line.strip())