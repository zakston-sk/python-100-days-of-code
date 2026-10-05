"""U.S. States Game (Day 25).

The player types U.S. state names. Correct guesses appear on a blank
map at the state's coordinates. Typing "Exit" saves the missed states
to a CSV file.
"""

from pathlib import Path

import pandas as pd
from turtle import Screen, Turtle, _Screen

# --- Paths -----------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
STATES_CSV = BASE_DIR / "50_states.csv"
MAP_IMAGE = BASE_DIR / "blank_states_img.gif"
MISSED_CSV = BASE_DIR / "missed_states.csv"

# --- Constants -------------------------------------------------------------
STATE_COLUMN = "state"
X_COLUMN = "x"
Y_COLUMN = "y"

FONT = ("Arial", 8, "normal")
ALIGNMENT = "center"
PROMPT_TITLE = "U.S. States Game"
PROMPT_TEXT = "Guess a state name (or type 'Exit'):"
EXIT_COMMAND = "exit"


# --- Data ------------------------------------------------------------------


def load_states(path: Path) -> pd.DataFrame:
    """Load the states CSV as a DataFrame."""
    return pd.read_csv(path)


def find_state(states: pd.DataFrame, name: str) -> pd.Series | None:
    """Return the row for the given state name, or None if not found."""
    match = states[states[STATE_COLUMN].str.lower() == name.lower()]
    if match.empty:
        return None
    return match.iloc[0]


def save_missed_states(states: pd.DataFrame, guessed: set[str]) -> None:
    """Write the states that were not guessed to a CSV file."""
    missed = states[~states[STATE_COLUMN].isin(guessed)][STATE_COLUMN]
    missed.to_csv(MISSED_CSV, index=False)


# --- UI --------------------------------------------------------------------


def build_screen(image_path: Path) -> _Screen:
    """Create the screen with the blank map as background."""
    screen = Screen()
    screen.title(PROMPT_TITLE)
    screen.setup(width=725, height=491)
    screen.bgpic(str(image_path))
    screen.tracer(0)
    return screen


def build_writer() -> Turtle:
    """Return a hidden turtle used to write state names on the map."""
    writer = Turtle()
    writer.hideturtle()
    writer.penup()
    writer.color("black")
    return writer


def draw_state(writer: Turtle, state: pd.Series) -> None:
    """Write the state name at its coordinates on the map."""
    writer.goto(state[X_COLUMN], state[Y_COLUMN])
    writer.write(state[STATE_COLUMN], align=ALIGNMENT, font=FONT)


# --- Game ------------------------------------------------------------------


def play(states: pd.DataFrame, screen: _Screen, writer: Turtle) -> set[str]:
    """Run the guessing loop and return the set of guessed states."""
    guessed: set[str] = set()
    total = len(states)

    while len(guessed) < total:
        answer = screen.textinput(
            title=f"{len(guessed)}/{total} States Correct",
            prompt=PROMPT_TEXT,
        )

        if answer is None or answer.strip().lower() == EXIT_COMMAND:
            break

        state = find_state(states, answer.strip())
        if state is None:
            continue

        name = state[STATE_COLUMN]
        if name in guessed:
            continue

        guessed.add(name)
        draw_state(writer, state)
        screen.update()

    return guessed


# --- Entry point -----------------------------------------------------------


def main() -> None:
    """Load data, set up the screen, and run the game."""
    states = load_states(STATES_CSV)
    screen = build_screen(MAP_IMAGE)
    writer = build_writer()

    guessed = play(states, screen, writer)

    if guessed:
        save_missed_states(states, guessed)
        print(f"Missed states saved to {MISSED_CSV}")

    screen.mainloop()


if __name__ == "__main__":
    main()
