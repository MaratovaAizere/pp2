#sub theme variables
x = 5
y = "John"
print(x)
print(y)
print(type(x))
print(type(y))

x = 4       # x is of type int
x = "Sally" # x is now of type str
print(x)

d = str(3)    # x will be '3'
f = int(3)    # y will be 3
z = float(3)  # z will be 3.0


#sub theme variable names
myvar = "John"
my_var = "John"
_my_var = "John"
myVar = "John"
MYVAR = "John"
myvar2 = "John"
"""
2myvar = "John"
my-var = "John"
my var = "John" <- error
"""


#sub theme Assign Multiple Values
a, b, c = "Orange", "Banana", "Cherry"
print(a)
print(b)
print(c)

e = k = l = "Orange"
print(e)
print(k)
print(l)

fruits = ["apple", "banana", "cherry"]
x1, y1, z1 = fruits
print(x1)
print(y1)
print(z1)


#sub theme Output Variables
q = "Python is awesome"
print(q)

x2 = "Python"
y2 = "is"
z2 = "awesome"
print(x2, y2, z2)

a1 = "Python "
b1 = "is "
c1 = "awesome"
print(a1 + b1 + c1)

x3 = 5
y3 = 10
print(x3 + y3)

x_ = 5
y_ = "John"
print(x_, y_)

#sub theme Global Variables
x = "awesome"

def myfunc():
  x = "fantastic"
  print("Python is " + x)

myfunc()

print("Python is " + x)