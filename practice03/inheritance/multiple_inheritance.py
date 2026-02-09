#1 Basic multiple inheritance
class A:
    def method_a(self):
        print("Method A")

class B:
    def method_b(self):
        print("Method B")

class C(A, B):
    pass

c = C()
c.method_a()
c.method_b()

#2 Multiple inheritance with attributes
class X:
    x = 10

class Y:
    y = 20

class Z(X, Y):
    pass

z = Z()
print(z.x, z.y)

#3 Multiple inheritance with constructors
class Parent1:
    def __init__(self):
        print("Parent1 init")

class Parent2:
    def __init__(self):
        print("Parent2 init")

class Child(Parent1, Parent2):
    def __init__(self):
        Parent1.__init__(self)
        Parent2.__init__(self)
        print("Child init")

Child()

#4 Multiple inheritance with super()
class Base1:
    def greet(self):
        print("Hello from Base1")

class Base2:
    def greet(self):
        print("Hello from Base2")

class Derived(Base1, Base2):
    def greet(self):
        super().greet()
        print("Hello from Derived")

Derived().greet()

#5 Diamond problem example
class A:
    def show(self):
        print("A")

class B(A):
    def show(self):
        print("B")

class C(A):
    def show(self):
        print("C")

class D(B, C):
    pass

d = D()
d.show() 