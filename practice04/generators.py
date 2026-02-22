def square(n):#ex1
    for i in range(1, n+1):
        yield i * i
n = int(input())

for i in square(n):
    print(i)

n = int(input())#ex2
print(*(i for i in range(0, n + 1, 2)), sep=",")

def devisible(n):#ex3
    for i in range(n + 1):
        if i % 3 == 0 and i%4 ==0:
            yield i
n=int(input())
for i in devisible(n):
    print(i)

def squares(a,b):#ex4
    for i in range(a, b+1):
        yield i * i
a=list(map(int,input().split()))
for i in squares(a[0],a[1]):
    print(i)

n=int(input())#ex5
print(*(i for i in range(n, -1, -1)), sep=" ")
