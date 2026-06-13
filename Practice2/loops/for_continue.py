# for loop with continue statement

# do not print banana
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  if x == "banana":
    continue
  print(x)

# skip even numbers
for i in range(1, 11):
  if i % 2 == 0:
    continue
  print(i)

# process only positive numbers
numbers = [5, -2, 8, -1, 3, 0]
for num in numbers:
  if i < 0:
    continue
  print(i)

# skip vowels
word = "programming"
for letter in word:
  if letter  in "eioau":
    continue
  print(letter)

# continue with condition
for i in range(10):
    if i < 5:
        continue
    print(i)
  
  