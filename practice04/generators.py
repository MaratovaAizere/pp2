#Task 1

def square(n):
    for i in range(1, n+1):
        yield i * i
n = int(input())

for i in square(n):
    print(i)

#Task 2

n = int(input())
print(*(i for i in range(0, n + 1, 2)), sep=",")

#Task 3

def devisible(n):
    for i in range(n + 1):
        if i % 3 == 0 and i%4 ==0:
            yield i
n=int(input())
for i in devisible(n):
    print(i)

#Task 4

def squares(a,b):
    for i in range(a, b+1):
        yield i * i
a=list(map(int,input().split()))
for i in squares(a[0],a[1]):
    print(i)

#Task 5

n=int(input())
print(*(i for i in range(n, -1, -1)), sep=" ")

#Iterators

#1

mytuple = ("apple", "banana", "cherry")
myit = iter(mytuple)

print(next(myit))
print(next(myit))
print(next(myit))

#2

mystr = "banana"
myit = iter(mystr)

print(next(myit))
print(next(myit))
print(next(myit))
print(next(myit))
print(next(myit))
print(next(myit))

#3

mytuple = ("apple", "banana", "cherry")

for x in mytuple:
  print(x)


#4

mystr = "banana"

for x in mystr:
  print(x)
