#1 Override method
class Animal:
    def sound(self):
        print("Generic sound")

class Cat(Animal):
    def sound(self):
        print("Meow")

Cat().sound()

#2 Override with different behavior
class Shape:
    def area(self):
        return 0

class Square(Shape):
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side * self.side

print(Square(4).area())

#3 Override with extended logic
class Person:
    def greet(self):
        print("Hello")

class Student(Person):
    def greet(self):
        print("Hello, I am a student")

Student().greet()

#4 Override with calculation
class Vehicle:
    def speed(self):
        return 50

class Car(Vehicle):
    def speed(self):
        return 100

print(Car().speed())

#5 Override with condition
class Account:
    def withdraw(self, amount):
        print(f"Withdrew {amount}")

class SavingsAccount(Account):
    def withdraw(self, amount):
        if amount > 1000:
            print("Limit exceeded")
        else:
            super().withdraw(amount)

SavingsAccount().withdraw(500)
SavingsAccount().withdraw(1500)