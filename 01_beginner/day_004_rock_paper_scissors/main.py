import random


rock = """
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
"""

paper = """
    _______
---'   ____)____
          ______)
          _______)
         _______)
---.__________)
"""

scissors = """
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
"""

choices = [rock, paper, scissors]

user_input = int(input("What do you choose? Type 0 for Rock, 1 for Paper or 2 for Scissors.\n"))
if user_input < 0 or user_input > 2:
    user_input = random.randint(0, 2)
print(choices[user_input])

computer_input = random.randint(0, 2)
print ("Computer chose:")
print(choices[computer_input])

result = user_input - computer_input
if result == 0:
    print("It's a draw.")
elif result == 1 or result == -2:
    print("You win!")
else:
    print("You lose.")
