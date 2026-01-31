# For loop with break statement

# Example 1: Break when finding "orange"
fruits = ["apple", "banana", "orange", "grape"]
for fruit in fruits:
    print(fruit)
    if fruit == "orange":
        break

# Example 2: Break at specific number
for i in range(10):
    if i == 6:
        break
    print(i)

# Example 3: Find first even number
numbers = [1, 3, 5, 8, 9, 2]
for num in numbers:
    if num % 2 == 0:
        print("First even:", num)
        break

# Example 4: Break in nested loop
for i in range(3):
    for j in range(3):
        if i == 1 and j == 1:
            break
        print(i, j)

# Example 5: Search for letter
text = "hello world"
for char in text:
    if char == "w":
        print("Found w")
        break
    print(char)