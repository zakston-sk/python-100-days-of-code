import random


DIFFICULTY_EASY = "easy"
DIFFICULTY_HARD = "hard"

DIFFICULTY = {
    DIFFICULTY_EASY: 10,
    DIFFICULTY_HARD: 5,
}


def print_greeting() -> None:
    """Print the greeting message."""
    print("Welcome to the Number Guessing Game!")
    print("I'm thinking of a number between 1 and 100.")


def print_goodbye() -> None:
    """Print the goodbye message."""
    print("Thank you for playing the Number Guessing Game!")
    print("Goodbye!")


def choose_difficulty() -> int:
    """Ask the user to choose a difficulty and return the attempt count."""
    while True:
        difficulty = input(
            f"Choose a difficulty. "
            f"Type '{DIFFICULTY_EASY}' or '{DIFFICULTY_HARD}': "
        ).strip().lower()

        if difficulty in DIFFICULTY:
            return DIFFICULTY[difficulty]

        print(
            f"Invalid choice. Please type "
            f"'{DIFFICULTY_EASY}' or '{DIFFICULTY_HARD}'."
        )


def get_random_number() -> int:
    """Return a random integer between 1 and 100."""
    return random.randint(1, 100)


def get_user_guess() -> int:
    """Ask the user for an integer between 1 and 100."""
    while True:
        try:
            guess = int(input("Make a guess: "))

            if 1 <= guess <= 100:
                return guess

            print("Please enter a number between 1 and 100.")
        except ValueError:
            print("Please enter a valid whole number.")


def play_round() -> None:
    """Play one round of the Number Guessing Game."""
    attempts = choose_difficulty()
    number_to_guess = get_random_number()

    print(f"You have {attempts} attempts to guess the number.")

    while attempts > 0:
        user_number = get_user_guess()

        if user_number == number_to_guess:
            print(
                f"Congratulations! You guessed the number "
                f"{number_to_guess}."
            )
            return

        if user_number < number_to_guess:
            print("Too low.")
        else:
            print("Too high.")

        attempts -= 1

        if attempts > 0:
            print(f"You have {attempts} attempts remaining.")

    print(f"You've run out of attempts. The number was {number_to_guess}.")
    print("Better luck next time!")
    print("Game over.")


def start_game() -> None:
    """Run rounds until the user decides to stop."""
    while True:
        play_round()

        play_again = input(
            "Do you want to play again? (yes/no): "
        ).strip().lower()

        if play_again not in ("yes", "y"):
            return


def main() -> None:
    """Run the Number Guessing Game."""
    print_greeting()
    start_game()
    print_goodbye()


if __name__ == "__main__":
    main()
