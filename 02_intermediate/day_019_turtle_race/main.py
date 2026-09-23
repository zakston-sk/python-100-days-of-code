"""Turtle Race (Day 20).

Six turtles race across the screen. The user bets on a colour,
and the winner is the first turtle to reach the right edge.
"""

import random
from turtle import Screen, Turtle

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 400
START_X = -230
FINISH_X = 230
STEP_MIN = 0
STEP_MAX = 10

COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
Y_POSITIONS = [-70, -40, -10, 20, 50, 80]


def create_turtles():
    """Create one turtle per colour and place them on the start line."""
    turtles = []
    for index, color in enumerate(COLORS):
        racer = Turtle(shape="turtle")
        racer.penup()
        racer.color(color)
        racer.goto(x=START_X, y=Y_POSITIONS[index])
        turtles.append(racer)
    return turtles


def run_race(turtles, user_bet):
    """Move each turtle until one of them crosses the finish line."""
    is_race_on = True

    while is_race_on:
        for racer in turtles:
            racer.forward(random.randint(STEP_MIN, STEP_MAX))

            if racer.xcor() > FINISH_X:
                is_race_on = False
                announce_winner(racer.pencolor(), user_bet)
                break


def announce_winner(winning_color, user_bet):
    """Print the result of the race based on the user's bet."""
    if winning_color == user_bet:
        print(f"You've won! The {winning_color} turtle is the winner!")
    else:
        print(f"You've lost! The {winning_color} turtle is the winner!")


def main():
    """Set up the screen, ask for a bet, and start the race."""
    screen = Screen()
    screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    screen.title("Turtle Race")

    user_bet = screen.textinput(
        title="Make your bet",
        prompt="Which turtle will win the race? Enter a color:",
    )

    turtles = create_turtles()

    if user_bet:
        run_race(turtles, user_bet)
    else:
        print("No bet placed — the race is cancelled.")

    screen.mainloop()


if __name__ == "__main__":
    main()
