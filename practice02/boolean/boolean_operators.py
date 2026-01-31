age = 18
answer = True

#Example 1. and
print(age >= 18 and answer)  # True

#Example 2. or
student = False
worker = True
print(student or worker)  # True

#Example 3. not
sunny = False
print(not sunny)  # True

#Example 4.
score=54
cheated = False
passed=score>=30 and not cheated
print(passed) #True

#Example 5.
age_client=14
ticket=True
can_enter= ticket and age_client>=18
print(can_enter) #False