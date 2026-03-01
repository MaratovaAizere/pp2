import re
# Example 1
print(re.split(r",", "apple,banana,cherry"))  # ['apple','banana','cherry']

# Example 2
print(re.split(r"[,;]", "apple,banana;cherry"))  # ['apple','banana','cherry']

# Example 3
print(re.split(r"\s+", "Total Amount Due"))  # ['Total','Amount','Due']

# Example 4
print(re.split(r"\d+", "Item1Item2Item3"))  # ['Item','Item','Item','']

# Example 5
print(re.split(r"\.", "www.example.com"))  # ['www','example','com']