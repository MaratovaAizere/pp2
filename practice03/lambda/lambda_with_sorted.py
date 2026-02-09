students = [("Emil", 25), ("Tobias", 22), ("Linus", 28)]
sorted_students = sorted(students, key=lambda x: x[1])
print(sorted_students)

ords = ["apple", "pie", "banana", "cherry"]
sorted_words = sorted(ords, key=lambda x: len(x))
print(sorted_words)