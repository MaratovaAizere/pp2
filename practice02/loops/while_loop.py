# Basic while loop examples

# Example 1: Count from 1 to 5
count = 1
while count <= 5:
    print(count)
    count = count + 1

# Example 2: Print even numbers under 10
num = 2
while num < 10:
    print(num)
    num = num + 2

# Example 3: Sum of first 5 numbers
total = 0
i = 1
while i <= 5:
    total = total + i
    i = i + 1
print("Sum is", total)

# Example 4: Reverse count
number = 5
while number > 0:
    print(number)
    number = number - 1

# Example 5: User input loop
password = ""
while password != "secret":
    password = "secret"  # Simplified for example
print("Access granted")