import random


letters = [
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
    "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
    "u", "v", "w", "x", "y", "z"
]
numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
symbols = ["!", "#", "$", "%", "&", "(", ")", "*", "+"]

print("Welcome to the Password Generator!")
letters_count = int(input("How many letters would you like in your password?\n"))
numbers_count = int(input("How many numbers would you like?\n"))
symbols_count = int(input("How many symbols would you like?\n"))

password_list = []
for _ in range(letters_count):
    password_list.append(random.choice(letters))
for _ in range(numbers_count):
    password_list.append(random.choice(numbers))
for _ in range(symbols_count):
    password_list.append(random.choice(symbols))
print(password_list)

# Shuffle
password_length = len(password_list)
for i in range(0, password_length):
    m = random.randint(0, password_length - 1)
    n = random.randint(0, password_length - 1)
    temp = password_list[m]
    password_list[m] = password_list[n]
    password_list[n] = temp
# random.shuffle(raw_password)
print(password_list)

password = ""
for character in password_list:
    password += character
# password = "".join(password_list)
print (f"Your password is: {password}")
