#Task 1
import math

degree = float(input("Input degree: "))
radian = degree * (math.pi / 180)

print("Output radian:", round(radian, 6))

#Task 2
height = float(input("Height: "))
base1 = float(input("Base, first value: "))
base2 = float(input("Base, second value: "))

area = ((base1 + base2) / 2) * height

print("Expected Output:", area)


#Task 3
import math

n = int(input("Input number of sides: "))
s = float(input("Input the length of a side: "))

area = (n * s * s) / (4 * math.tan(math.pi / n))

print("The area of the polygon is:", round(area))


#Task 4
base = float(input("Length of base: "))
height = float(input("Height of parallelogram: "))

area = base * height

print("Expected Output:", area)
