# While loop with continue statement

# Example 1: Skip odd numbers
num = 0
while num < 10:
    num = num + 1
    if num % 2 != 0:
        continue
    print(num)

# Example 2: Skip specific value
count = 0
while count < 5:
    count = count + 1
    if count == 3:
        continue
    print(count)

# Example 3: Process only positive numbers
numbers = [5, -2, 8, -1, 3]
i = 0
while i < len(numbers):
    if numbers[i] < 0:
        i = i + 1
        continue
    print("Processing:", numbers[i])
    i = i + 1

# Example 4: Skip vowels in string
text = "hello"
index = 0
while index < len(text):
    if text[index] in "aeiou":
        index = index + 1
        continue
    print(text[index])
    index = index + 1

# Example 5: Continue until condition met
value = 0
while value < 10:
    value = value + 1
    if value < 5:
        continue
    print(value)