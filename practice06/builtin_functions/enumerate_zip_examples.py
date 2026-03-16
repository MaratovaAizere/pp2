# enumerate_zip_examples.py

names = ["Alice", "Bob", "Charlie"]
scores = [85, 90, 78]

# enumerate
print("Using enumerate:")
for index, name in enumerate(names):
    print(index, name)

# zip
print("\nUsing zip:")
for name, score in zip(names, scores):
    print(name, score)

# type checking
value = "123"

print("\nType of value:", type(value))

# type conversion
num = int(value)
print("Converted to int:", num)