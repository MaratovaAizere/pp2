import re
# Example 1
print(re.search(r"\d+", "Items: 12, 7, 3").group())  # 12

# Example 2
print(re.search(r"[A-Z][a-z]+", "Total Amount").group())  # Total

# Example 3
print(re.search(r"\w+@\w+\.\w+", "Email: test@mail.com").group())  # test@mail.com

# Example 4
print(re.search(r"\$\d+\.\d{2}", "Price: $45.67").group())  # $45.67

# Example 5
reg=r"(\d{4}-\d{2}-\d{2}) (\d{4}-\d{2}-\d{2})"
r=re.search(reg, "Date: 2026-02-27 2025-06-18")
if r:
    print(' '.join(r.groups()))