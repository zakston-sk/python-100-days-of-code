"""Scoreboard for the Pong game (Day 22)."""

from turtle import Turtle

import settings


class Scoreboard(Turtle):
    """Displays the score, pause, and game-over messages."""

    def __init__(self) -> None:
        super().__init__()
        self.l_score = 0
        self.r_score = 0
        self.color(settings.SCORE_COLOR)
        self.penup()
        self.hideturtle()
        self.update_display()

    def update_display(self) -> None:
        """Redraw the score at the top of the screen."""
        self.clear()
        self.goto(settings.SCORE_POSITION)  # always reset position
        self.write(
            f"{self.l_score}   {self.r_score}",
            align="center",
            font=settings.SCORE_FONT,
        )

    def point_left(self) -> None:
        """Increment the left player's score."""
        self.l_score += 1
        self.update_display()

    def point_right(self) -> None:
        """Increment the right player's score."""
        self.r_score += 1
        self.update_display()

    def reset(self) -> None:
        """Reset both scores to zero."""
        self.l_score = 0
        self.r_score = 0
        self.update_display()

    def game_winner(self) -> str | None:
        """Return 'left', 'right', or None if nobody has won yet."""
        if self.l_score >= settings.WINNING_SCORE:
            return "left"
        if self.r_score >= settings.WINNING_SCORE:
            return "right"
        return None

    def show_game_over(self, winner: str) -> None:
        """Show the game-over message in the centre of the screen."""
        self.goto(0, 100)
        self.write(
            f"GAME OVER - {winner.upper()} PLAYER WINS!  (press R to restart)",
            align="center",
            font=settings.SCORE_GAME_OVER_FONT,
        )

    def show_pause(self) -> None:
        """Show the pause message in the centre of the screen."""
        self.goto(0, 0)
        self.write(
            "PAUSED - press SPACE to resume",
            align="center",
            font=settings.PAUSE_FONT,
        )
