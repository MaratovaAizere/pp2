numbers = [1, 2, 3, 4, 5, 6, 7, 8]
odd_numbers = list(filter(lambda x: x % 2 != 0, numbers))
print(odd_numbers)

names = ["Oleg", "Azamat", "Adiya", "Arkadiy", "Zhiger"]
odd_names = list(filter(lambda x: len(x) % 2 != 0, names))
print(odd_names)

statements = [True, True, False, True, True]
doubled = list(filter(lambda x: x != True, statements))
print(doubled)