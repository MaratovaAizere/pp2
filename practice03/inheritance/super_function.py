#1 Using super() to call parent constructor
class Person:
    def __init__(self, name):
        self.name = name

class Student(Person):
    def __init__(self, name, subject):
        super().__init__(name)
        self.subject = subject

s = Student("Bekzat", "Python")
print(s.name, s.subject)

#2 super() in method
class Animal:
    def sound(self):
        print("Generic sound")

class Dog(Animal):
    def sound(self):
        super().sound()
        print("Woof!")

Dog().sound()

#3 super() with multiple attributes
class Vehicle:
    def __init__(self, brand):
        self.brand = brand

class Car(Vehicle):
    def __init__(self, brand, year):
        super().__init__(brand)
        self.year = year

c = Car("Toyota", 2020)
print(c.brand, c.year)

#4 super() in overridden method
class Parent:
    def show(self):
        print("Parent show")

class Child(Parent):
    def show(self):
        super().show()
        print("Child show")

Child().show()

#5 super() with default values
class Base:
    def __init__(self, x=0):
        self.x = x

class Derived(Base):
    def __init__(self, x, y):
        super().__init__(x)
        self.y = y

d = Derived(5, 10)
print(d.x, d.y)