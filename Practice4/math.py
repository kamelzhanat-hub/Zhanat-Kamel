import math

# task 1

degree = float(input())
radian = degree * (math.pi / 180)

print(round(radian, 6))

# task 2

height = float(input("Height: "))
base1 = float(input("Base, first value: "))
base2 = float(input("Base, second value: "))

area = ((base1 + base2) / 2) * height

print("Expected Output:", area)

# task 3

n = int(input("Input number of sides: "))
s = float(input("Input the length of a side: "))

area = (n * s * s) / (4 * math.tan(math.pi / n))

print("The area of the polygon is:", round(area))

# task 4

base = float(input("Length of base: "))
height = float(input("Height of parallelogram: "))

area = base * height

print("Expected Output:", area)