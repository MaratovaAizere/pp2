#syntax: lambda arguments : expression
x = lambda a : a + 10
print(x(5))
x = lambda a, b : a * b
print(x(5, 6))

def myfunc(n):
    return lambda a : a * n

mytripler = myfunc(3) #mytripler saves lambda a : a * 3 and then recalls a as 11

print(mytripler(11))

#i can use multiple functions
def myfunc(n):
  return lambda a : a * n

mydoubler = myfunc(2)
mytripler = myfunc(3)

print(mydoubler(11))
print(mytripler(11))
