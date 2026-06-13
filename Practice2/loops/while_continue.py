# while loop with continue statement

# continue if i = 3
i = 1
while i < 5:
    print(i)
    if i == 3: 
        continue
    i += 1

# skip odd numbers
i = 1
while i < 10:
    if i % 2 != 0:
        i += 1  
        continue
    print(i)
    i += 1  

# process only positive numbers
numbers = [5, -2, 8, -1, 3]
i = 0
while i < len(numbers):
    if numbers[i] < 0:
        i = i + 1
        continue
    print("Processing:", numbers[i])
    i = i + 1

# skip vowels in string
text = "hello"
index = 0
while index < len(text):
    if text[index] in "aeiou":
        index = index + 1
        continue
    print(text[index])
    index = index + 1

