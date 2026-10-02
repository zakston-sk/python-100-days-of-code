"""Car sprite for the Turtle Crossing game (Day 23)."""

from random import choice, randint
from turtle import Turtle

import settings


class Car(Turtle):
    """A car that drives from right to left across the screen."""

    def __init__(self, position: tuple[float, float]) -> None:
        super().__init__(shape="square")
        self.penup()
        self.speed(settings.CAR_SPEED)
        self.color(choice(settings.CAR_COLORS))
        self.setheading(settings.CAR_HEADING)
        self.goto(position)
        self.move_speed = randint(
            settings.CAR_MIN_MOVE_SPEED,
            settings.CAR_MAX_MOVE_SPEED,
        )
        self.shapesize(
            stretch_wid=settings.CAR_W / 20,
            stretch_len=settings.CAR_H / 20,
        )

    def update(self, dt: float) -> None:
        """Move the car left by its speed scaled by delta time."""
        new_x = self.xcor() - self.move_speed * dt
        self.goto(new_x, self.ycor())

    def respawn(self, position: tuple[float, float]) -> None:
        """Reset a recycled car with a fresh position, colour, and speed."""
        self.color(choice(settings.CAR_COLORS))
        self.move_speed = randint(
            settings.CAR_MIN_MOVE_SPEED,
            settings.CAR_MAX_MOVE_SPEED,
        )
        self.goto(position)
        self.showturtle()
