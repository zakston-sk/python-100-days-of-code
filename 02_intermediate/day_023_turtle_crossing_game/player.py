"""Player-controlled turtle for the Turtle Crossing game (Day 23)."""

from turtle import Turtle

import settings


class Player(Turtle):
    """A turtle that moves in steps and tries to reach the top of the screen."""

    def __init__(self, position: tuple[float, float]) -> None:
        super().__init__(shape="turtle")
        self.penup()
        self.speed(settings.PLAYER_SPEED)
        self.color(settings.PLAYER_COLOR)
        self.setheading(settings.PLAYER_HEADING)
        self.goto(position)

    def move_up(self) -> None:
        """Move the player one step up."""
        self.sety(self.ycor() + settings.PLAYER_STEP)

    def move_down(self) -> None:
        """Move the player one step down, clamped to the bottom edge."""
        min_y = -settings.SCREEN_H / 2 + settings.PLAYER_STEP
        self.sety(max(self.ycor() - settings.PLAYER_STEP, min_y))

    def move_left(self) -> None:
        """Move the player one step left, clamped to the left edge."""
        min_x = -settings.SCREEN_W / 2 + settings.PLAYER_STEP
        self.setx(max(self.xcor() - settings.PLAYER_STEP, min_x))

    def move_right(self) -> None:
        """Move the player one step right, clamped to the right edge."""
        max_x = settings.SCREEN_W / 2 - settings.PLAYER_STEP
        self.setx(min(self.xcor() + settings.PLAYER_STEP, max_x))

    def has_finished(self) -> bool:
        """Return True if the player has crossed the finish line."""
        return self.ycor() > settings.PLAYER_FINISH_LINE_Y

    def reset(self) -> None:
        """Return the player to the starting position."""
        self.goto(settings.PLAYER_START_POSITION)
