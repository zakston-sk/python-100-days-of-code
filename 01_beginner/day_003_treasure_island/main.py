import logo


print(logo.logo)
print("Welcome to Treasure Island.")
print("Your mission is to find the treasure.")

print("You're at a cross road. Where do you want to go?")
user_input = input("Type \"left\" or \"right\":\n").lower()

if user_input == "left":
    print("You've come to a lake. There is an island in the middle of the lake.")
    user_input = input("Type \"wait\" to wait for a boat. Type \"swim\" to swim across.\n").lower()

    if user_input == "wait":
        print("You arrive at the island unharmed. There is a house with 3 doors.")
        user_input = input("One red, one yellow and one blue. Which colour do you choose?\n").lower()
        
        if user_input == "red":
            print("It's a room full of fire. Game Over.")
        elif user_input == "yellow":
            print("You found the treasure! You Win!")
        else:
            print("You enter a room of beasts. Game Over.")
    else:
        print("You get attacked by an angry trout. Game Over.")
else:
    print("You fell into a hole. Game Over.")
