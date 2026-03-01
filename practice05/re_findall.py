import re
text = "12, 7, 3"

# Example 1
print(re.findall(r"\d+", text))  # ['12','7','3']

# Example 2
print(re.findall(r"[A-Z][a-z]+", "Total Amount Tax"))  # ['Total','Amount','Tax']

# Example 3
print(re.findall(r"\w+@\w+\.\w+", "a@x.com b@y.org"))  # ['a@x.com','b@y.org']

# Example 4
print(re.findall(r"\$\d+\.\d{2}", "Prices: $45.67 $30.00"))  # ['$45.67','$30.00']

# Example 5
print(re.findall(r"[aeiou]", "hello world"))  # ['e','o','o']