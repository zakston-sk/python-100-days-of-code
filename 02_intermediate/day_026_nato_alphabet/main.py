"""NATO Phonetic Alphabet (Day 26).

Converts a word into its NATO phonetic alphabet equivalent
(e.g. "hello" -> ["Hotel", "Echo", "Lima", "Lima", "Oscar"]).
"""

from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
NATO_CSV = BASE_DIR / "nato_phonetic_alphabet.csv"
LETTER_COLUMN = "letter"
CODE_COLUMN = "code"
QUIT_COMMAND = "q"


def load_alphabet(path: Path) -> dict[str, str]:
    """Load the NATO alphabet CSV as a {letter: code} dictionary."""
    data = pd.read_csv(path)
    return {row[LETTER_COLUMN]: row[CODE_COLUMN] for _, row in data.iterrows()}


def to_nato(word: str, alphabet: dict[str, str]) -> list[str]:
    """Return the NATO code words for the given word.

    Non-alphabetic characters (spaces, punctuation) are skipped.
    """
    return [alphabet[letter] for letter in word.upper() if letter in alphabet]


def main() -> None:
    """Run the interactive NATO translator."""
    alphabet = load_alphabet(NATO_CSV)

    while True:
        user_input = input("Enter a word (or q to quit): ").strip()

        if user_input.lower() == QUIT_COMMAND:
            print("Goodbye!")
            break

        print(to_nato(user_input, alphabet), "\n")


if __name__ == "__main__":
    main()
