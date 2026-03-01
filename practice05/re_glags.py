import re
# Example 1 - IGNORECASE
print(re.search(r"total", "TOTAL: $45.67", re.IGNORECASE).group())  # TOTAL

# Example 2 - MULTILINE
text = "Total: $45.67\nSubtotal: $30.00"
print(re.findall(r"^\w+:", text, re.MULTILINE))  # ['Total:', 'Subtotal:']

# Example 3 - DOTALL
print(re.search(r"Total:.*30.00", text, re.DOTALL).group())  # Total: $45.67\nSubtotal: $30.00

# Example 4 - IGNORECASE with findall
print(re.findall(r"total", "TOTAL total Total", re.IGNORECASE))  # ['TOTAL','total','Total']

# Example 5 - MULTILINE start of line
text2 = "Date: 2026-02-27\nInvoice: #12345"
print(re.findall(r"^Invoice:.*", text2, re.MULTILINE))  # ['Invoice: #12345']