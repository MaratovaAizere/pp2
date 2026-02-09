# class in object constructor
class MyClass:
    x = 5
p1 = MyClass()
print(p1.x)
#created object p1
del p1
#deleted p1
#we can create as many classes as we want
p1 = MyClass()
p2 = MyClass()
p3 = MyClass()

print(p1.x)
print(p2.x)
print(p3.x)
#class cant be empty, use pass
class Person:
  pass
  