"""Centre net for the Pong game (Day 22)."""

from turtle import Turtle

import settings


class Net(Turtle):
    """A dashed vertical line in the middle of the screen."""

    def __init__(self) -> None:
        super().__init__()
        self.color(settings.NET_COLOR)
        self.pensize(3)
        self.penup()
        self.hideturtle()
        self.speed(0)
        self._draw()

    def _draw(self) -> None:
        """Draw the dashed line from top to bottom."""
        dash = settings.NET_DASH_LENGTH
        gap = settings.NET_GAP_LENGTH
        y = settings.SCREEN_HEIGHT / 2
        self.goto(0, y)
        self.setheading(270)
        while y > -settings.SCREEN_HEIGHT / 2:
            self.pendown()
            self.forward(dash)
            self.penup()
            self.forward(gap)
            y -= dash + gap
