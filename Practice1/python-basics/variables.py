a = 13
b = "python"
print(a)
print(b)

#casting
d = str(5)
f = float(5)
g = int(5)
 
print(d)
print(f)
print(g)

#legal variable names
myvar = "John"
my_var = "John"
_my_var = "John"
myVar = "John"
MYVAR = "John"
myvar2 = "John"

#multiple variables
x, y, z = "Orange", "Banana", "Cherry"
print(x)
print(y)
print(z)

#one value to multiple variables
x = y = z = "Orange"
print(x)
print(y)
print(z)

#list
fruits = ["apple", "banana", "cherry"]
x, y, z = fruits
print(x)
print(y)
print(z)

#global vsriable
k = "hello world"

def func():
    print(k)

func()

