# While loop with break statement

# Example 1: Break when number equals 5
num = 1
while num <= 10:
    print(num)
    if num == 5:
        break
    num = num + 1

# Example 2: Find first multiple of 7
number = 1
while True:
    if number % 7 == 0:
        print("Found:", number)
        break
    number = number + 1

# Example 3: Password attempt limit
attempts = 0
while attempts < 3:
    password = "try123"  # User would input here
    if password == "secret":
        print("Correct password")
        break
    attempts = attempts + 1
else:
    print("Too many attempts")

# Example 4: Sum until negative number
total = 0
while True:
    num = 5  # Would be user input
    if num < 0:
        break
    total = total + num
print("Total sum:", total)

# Example 5: Break in nested loop
i = 1
while i <= 3:
    j = 1
    while j <= 3:
        print(i, j)
        if i == 2 and j == 2:
            print("Breaking inner loop")
            break
        j = j + 1
    i = i + 1