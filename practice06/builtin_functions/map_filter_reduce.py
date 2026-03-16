# map_filter_reduce.py

from functools import reduce

numbers = [1, 2, 3, 4, 5, 6]

# map
squared = list(map(lambda x: x**2, numbers))
print("Squared numbers:", squared)

# filter
even = list(filter(lambda x: x % 2 == 0, numbers))
print("Even numbers:", even)

# reduce
sum_all = reduce(lambda a, b: a + b, numbers)
print("Sum using reduce:", sum_all)