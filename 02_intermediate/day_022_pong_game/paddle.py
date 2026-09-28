"""Paddle for the Pong game (Day 22)."""

from turtle import Turtle

import settings


class Paddle(Turtle):
    """A vertical paddle controlled by the player."""

    def __init__(self, position: tuple[float, float]) -> None:
        super().__init__(shape="square")
        self.color(settings.PADDLE_COLOR)
        self.shapesize(
            stretch_wid=settings.PADDLE_HEIGHT / 20,
            stretch_len=settings.PADDLE_WIDTH / 20,
        )
        self.penup()
        self.goto(position)
        self.speed(0)

    def move_up(self, dt: float) -> None:
        """Move the paddle up, clamped to the screen."""
        new_y = self.ycor() + settings.PADDLE_SPEED * dt
        max_y = settings.SCREEN_HEIGHT / 2 - settings.PADDLE_HEIGHT / 2
        self.goto(self.xcor(), min(new_y, max_y))

    def move_down(self, dt: float) -> None:
        """Move the paddle down, clamped to the screen."""
        new_y = self.ycor() - settings.PADDLE_SPEED * dt
        min_y = -(settings.SCREEN_HEIGHT / 2 - settings.PADDLE_HEIGHT / 2)
        self.goto(self.xcor(), max(new_y, min_y))

    def reset_position(self) -> None:
        """Return the paddle to the vertical centre."""
        self.goto(self.xcor(), 0)
