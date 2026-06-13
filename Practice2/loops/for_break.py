# for loop with break statement

# exit the loop if x is "banana"
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  print(x)
  if x == "banana":
    break

# break at specific number
for i in range(10):
  if i == 5:
    break
  print(i)

# find first even number
nums = [1, 3 , 6 , 7, 9, 2]
for num in nums:
  if num % 2 == 0:
    print(num)
    break

# break in nested loop
for i in range(3):
  for j in range(3):
    if i == 1 and j == 1:
      break
    print(i, j)

# search for letter
text = "hello world"
for char in text:
    if char == "w":
        print("Found w")
        break
    print(char)

