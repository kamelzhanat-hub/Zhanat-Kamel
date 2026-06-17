# a function with one argument
def my_function(fname):
  print(fname + " Refsnes")

my_function("Emil")
my_function("Tobias")
my_function("Linus")

# parameter - argument perspective
def hi_to_function(name):
    print("Hello", name) #name is a parameter

hi_to_function("Emil") #Emil is an argument

# we can use several arguments
def my_function(fname, lname):
  print(fname + " " + lname)

my_function("Emil", "Refsnes")

# we can assign default values to parameters
def my_function(name = "friend"):
  print("Hello", name)

my_function("Emil")
my_function("Tobias")
my_function()
my_function("Linus")

# we can use key - value system
def my_function(animal, name):
  print("I have a", animal)
  print("My", animal + "'s name is", name)

my_function(animal = "dog", name = "Buddy")

# positional arguments
# calling a function with arguments without using keywords
# positional arguments must be in the correct order
def my_function(animal, name):
  print("I have a", animal)
  print("My", animal + "'s name is", name)

my_function("dog", "Buddy")

# we can put in lists
def my_function(fruits):
  for fruit in fruits:
    print(fruit)

my_fruits = ["apple", "banana", "cherry"]
my_function(my_fruits)

# return value
def my_function(x, y):
  return x + y


# arguments before / are positional-only, and arguments after * are keyword-only:
result = my_function(5, 3)
print(result)

def my_function(a, b, /, *, c, d):
  return a + b + c + d

result = my_function(5, 10, c = 15, d = 20)
print(result)