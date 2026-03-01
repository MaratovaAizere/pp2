import re
# Example 1
print(re.sub(r"\$", "USD", "Total: $45.67"))  # Total: USD45.67

# Example 2
print(re.sub(r"\d+", "#", "Invoice 12345"))  # Invoice #####

# Example 3
print(re.sub(r"[aeiou]", "*", "hello"))  # h*ll*

# Example 4
print(re.sub(r"\s+", "_", "Total Amount Due"))  # Total_Amount_Due

# Example 5
print(re.sub(r"\w+@\w+\.\w+", "EMAIL", "Contact: test@mail.com"))  # Contact: EMAIL