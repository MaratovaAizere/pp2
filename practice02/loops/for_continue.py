# For loop with continue statement

# Example 1: Skip even numbers
for i in range(1, 11):
    if i % 2 == 0:
        continue
    print(i)

# Example 2: Skip specific item
fruits = ["apple", "banana", "orange", "grape"]
for fruit in fruits:
    if fruit == "banana":
        continue
    print(fruit)

# Example 3: Process only positive numbers
numbers = [5, -2, 8, -1, 3, 0]
for num in numbers:
    if num <= 0:
        continue
    print("Positive:", num)

# Example 4: Skip vowels
text = "programming"
for char in text:
    if char in "aeiou":
        continue
    print(char)

# Example 5: Continue with condition
for i in range(10):
    if i < 5:
        continue
    print(i)