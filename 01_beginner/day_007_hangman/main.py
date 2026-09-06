import random
import hangman_words
from hangman_art import logo, stages

print(logo)

words = [
    hangman_words.easy_words,
    hangman_words.medium_words,
    hangman_words.hard_words,
]

print("Choose difficulty:")
print("0 - Easy")
print("1 - Medium")
print("2 - Hard")

difficulty = -1
while difficulty not in [0, 1, 2]:
    choice = input("Enter your choice (0, 1, or 2): ")
    if choice.isdigit():
        difficulty = int(choice)
        if difficulty not in [0, 1, 2]:
            print("Please enter 0, 1, or 2.")
    else:
        print("Please enter a valid number (0, 1, or 2).")

word_list = words[difficulty]
secret_word = random.choice(word_list)
lives = 6
guessed_letters = []
guessed = False
placeholder = "_" * len(secret_word)

while lives > 0 and not guessed:
    print(f"Word to guess: {placeholder}")
    guess = input("Guess a letter: ").lower()

    # Проверка, что пользователь ввёл только одну букву
    if len(guess) != 1 or not guess.isalpha():
        print("Please enter a single letter.")
        continue

    while guess in guessed_letters:
        print(f"You've already guessed '{guess}'. Try again.")
        guess = input("Guess a letter: ").lower()

    guessed_letters.append(guess)

    if guess in secret_word:
        placeholder = ""
        for letter in secret_word:
            if letter in guessed_letters:
                placeholder += letter
            else:
                placeholder += "_"
        if "_" not in placeholder:
            guessed = True
    else:
        print(f"You guessed '{guess}', that's not in the word. You lose a life.")
        lives -= 1
        print(stages[lives])
        if lives > 0:
            print(f"{lives} lives left.")

if guessed:
    print("You win!")
else:
    print("You lose.")
