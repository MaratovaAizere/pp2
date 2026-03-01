import re

text = "Total: $45.67"

# Example 1
print(re.search(r"\d+\.\d+", text).group())  # 45.67

# Example 2
text2 = "Invoice #12345"
print(re.findall(r"\d+", text2))  # ['12345']

# Example 3
text3 = "Contact: test@mail.com"
print(re.search(r"\w+@\w+\.\w+", text3).group())  # test@mail.com

# Example 4
text4 = "Subtotal: $30.50"
print(re.findall(r"\$\d+\.\d{2}", text4))  # ['$30.50']

# Example 5
text5 = "Date: 2026-02-27"
print(re.search(r"\d{4}-\d{2}-\d{2}", text5).group())  # 2026-02-27