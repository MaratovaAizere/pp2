import re
# Example 1
print(re.match(r"Total", "Total: $45.67"))  # Match object

# Example 2
print(re.match(r"Invoice", "Invoice #12345").group())  # Invoice

# Example 3
print(re.match(r"\d+", "123 Items"))  # Match object

# Example 4
print(re.match(r"[A-Z][a-z]+", "Hello World").group())  # Hello

# Example 5
print(re.match(r"^Date", "Date: 2026-02-27").group())  # Date