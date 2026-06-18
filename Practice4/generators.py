# task 1
def sqr(num):
    n = 1
    while n < num:
        yield n ** 2
        n += 1
num = int(input())

for a in sqr(num):
    print(a)
        
# task 2
n = int(input())

def lrt(n):
    for i in range(0, n + 1):  
        if i % 2 == 0:
            yield i

print(*lrt(n), sep=", ")

# task 3
def devisible(n):
    for i in range(n + 1):
        if i % 3 == 0 and i%4 ==0:
            yield i
n=int(input())

for i in devisible(n):
    print(i)

# task 4
a = int(input())
b = int(input())
def squares(a, b):
    for i in range(a, b + 1):
            yield i ** 2

for i in squares(a, b):
    print(i)

# task 5
def zxc(n):  
    while n >= 0: 
        yield n
        n -= 1

n = int(input())

for a in zxc(n):
    print(a)

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