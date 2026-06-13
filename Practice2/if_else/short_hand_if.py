#if we have only one statement to execute, we can put it on the same line as the if statement.
a = 5
b = 2
if a > b: print("a is greater than b")

#short hand if else
a = 2
b = 330
print("A") if a > b else print("B")

# in python we have short hand if and else, this is called a conditional expression ("ternary operator").
a = 10
b = 20
bigger = a if a > b else b
print("Bigger is", bigger)