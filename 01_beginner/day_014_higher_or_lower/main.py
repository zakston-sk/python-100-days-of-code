import random
from art import logo, vs
from game_data import data


def clear_screen() -> None:
    """Clear the console screen using ANSI escape codes."""
    print("\033[H\033[J", end="")


def format_person(person, label):
    """Return a formatted string with a person's name, description, and country."""
    return (
        f"{label}: {person['name']}"
        f"[{person['description']}, from {person['country']}]"
    )


def get_random_person(exclude):
    """Return a random person from the data, optionally excluding one by name."""
    person = random.choice(data)
    if exclude is not None:
        while person["name"] == exclude["name"]:
            person = random.choice(data)
    return person


def get_user_input():
    """Prompt the user to choose 'A' or 'B' and return a valid choice."""
    while True:
        choice = input("Who has more followers? Type 'A' or 'B': ").strip().lower()
        if choice in ("a", "b"):
            return choice
        print("Invalid choice. Please type 'A' or 'B'.")


def get_correct_answer(person_a, person_b):
    """Return 'a' if person A has more followers, otherwise 'b'."""
    return "a" if person_a["follower_count"] > person_b["follower_count"] else "b"


def play_round(person_a, person_b):
    print(format_person(person_a, "Compare A"))
    print(vs)
    print(format_person(person_b, "Against B"))

    user_input = get_user_input()
    correct_answer = get_correct_answer(person_a, person_b)

    return user_input == correct_answer


def main():
    print(logo)
    print()

    score = 0
    running = True
    person_a = random.choice(data)

    while running:
        person_b = get_random_person(person_a)
        running = play_round(person_a, person_b)

        if running:
            person_a = person_b
            clear_screen()
            score += 1
            print(f"You're right! Current score: {score}.")

    print(f"Sorry, that's wrong. Final score: {score}")


if __name__ == "__main__":
    main()