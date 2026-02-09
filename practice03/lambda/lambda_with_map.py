#each element of numbers list is multiplied by 2
numbers = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, numbers))
print(doubled)

names = ["A", "B", "C", "D", "E"]
doubled = list(map(lambda x: x * 2, names))
print(doubled)

statements = [True, True, False, True, True]
doubled = list(map(lambda x: True if x == False else False, statements))
print(doubled)