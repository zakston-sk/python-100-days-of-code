"""Food class for the Snake Game (Day 21)."""

from random import randint
from turtle import Turtle

GRID_SIZE = 20
# Centres of cells are at -280, -260, ..., 260, 280
MAX_CELL = 14  # 14 * 20 = 280


class Food(Turtle):
    """A piece of food placed at the centre of a grid cell."""

    def __init__(self) -> None:
        super().__init__()
        self.shape("square")
        self.color("red")
        self.penup()
        self.speed("fastest")
        self.refresh()

    def refresh(self) -> None:
        """Move the food to a random cell centre (multiple of GRID_SIZE)."""
        cell_x = randint(-MAX_CELL, MAX_CELL)
        cell_y = randint(-MAX_CELL, MAX_CELL)
        self.goto(cell_x * GRID_SIZE, cell_y * GRID_SIZE)
