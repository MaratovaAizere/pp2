#Task 1
def squares(n):
    for i in range(1, n + 1):
        yield i * i

# пример использования
N = 5
for sq in squares(N):
    print(sq)

#Task 2
def jup_sandar(n):
    for i in range(0,n+1):
        if i%2==0:
            yield i
    
n=int(input())
print(",".join(map(str, jup_sandar(n))))

#Task 3
def number(n):
    for i in range(0, n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i

n = int(input())
for x in number(n):
    print(x, end=" ")

#Task 4
def square(a, b):
    for i in range(a, b + 1):
        yield i * i

# тест
a = 3
b = 7
for val in square(a, b):
    print(val)


#Task 5
def countdown(n):
    for i in range(n, -1, -1):
        yield i

n = int(input())
for x in countdown(n):
    print(x, end=" ")