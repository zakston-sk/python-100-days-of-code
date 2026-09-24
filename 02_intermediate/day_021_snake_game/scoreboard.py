"""Scoreboard class for the Snake Game (Day 21)."""

from turtle import Turtle

FONT = ("Arial", 14, "bold")
ALIGNMENT = "center"
SCORE_POSITION = (0, 270)


class Scoreboard(Turtle):
    """Displays the current score and the game-over message."""

    def __init__(self) -> None:
        super().__init__()
        self.score = 0
        self.hideturtle()
        self.penup()
        self.color("white")
        self.goto(SCORE_POSITION)
        self.update()

    def increase_score(self) -> None:
        """Increment the score and refresh the display."""
        self.score += 1
        self.update()

    def update(self) -> None:
        """Clear and redraw the score text."""
        self.clear()
        self.write(f"Score: {self.score}", align=ALIGNMENT, font=FONT)

    def game_over(self) -> None:
        """Show the game-over message in the centre of the screen."""
        self.goto(0, 0)
        self.write("GAME OVER", align=ALIGNMENT, font=FONT)
