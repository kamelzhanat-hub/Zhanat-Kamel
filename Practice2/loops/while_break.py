# while loop with break statement

# break if a num equals 5
i = 1
while i <= 10:
    print(i)
    if i == 5:
        break
    i += 1

# find the first multiple of 7
number = 1
while True:
    if number % 7 == 0:
        print("Found:", number)
        break
    number = number + 1

# password attempt limit
attempts = 0
while attempts < 3:
    password = "try123"  # User would input here
    if password == "secret":
        print("Correct password")
        break
    attempts = attempts + 1
else:
    print("Too many attempts")

# sum until negative number
total = 0
while True:
    num = 5  # Would be user input
    if num < 0:
        break
    total = total + num
print("Total sum:", total)


