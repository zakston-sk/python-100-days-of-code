"""Snake class for the Snake Game (Day 21)."""

from turtle import Turtle

GRID_SIZE = 20
STARTING_POSITIONS = [(0, 0), (-GRID_SIZE, 0), (-2 * GRID_SIZE, 0)]
MOVE_DISTANCE = GRID_SIZE

UP = 90
DOWN = 270
LEFT = 180
RIGHT = 0


class Snake:
    """A snake made of square turtle segments."""

    def __init__(self) -> None:
        self.body: list[Turtle] = []
        self._create_snake()
        self.head = self.body[0]

    def _create_snake(self) -> None:
        """Create the initial three segments of the snake."""
        for position in STARTING_POSITIONS:
            self.add_segment(position)

    def add_segment(self, position: tuple) -> None:
        """Add a new segment at the given position."""
        segment = Turtle("square")
        segment.color("white")
        segment.penup()
        segment.goto(position)
        self.body.append(segment)

    def eat(self) -> None:
        """Grow the snake by adding a segment at the tail."""
        self.add_segment(self.body[-1].position())

    def move(self) -> None:
        """Move the snake forward by one grid cell."""
        for index in range(len(self.body) - 1, 0, -1):
            x = self.body[index - 1].xcor()
            y = self.body[index - 1].ycor()
            self.body[index].goto(x, y)
        self.head.forward(MOVE_DISTANCE)

    def up(self) -> None:
        """Turn the snake up (unless it is moving down)."""
        if self.head.heading() != DOWN:
            self.head.setheading(UP)

    def down(self) -> None:
        """Turn the snake down (unless it is moving up)."""
        if self.head.heading() != UP:
            self.head.setheading(DOWN)

    def left(self) -> None:
        """Turn the snake left (unless it is moving right)."""
        if self.head.heading() != RIGHT:
            self.head.setheading(LEFT)

    def right(self) -> None:
        """Turn the snake right (unless it is moving left)."""
        if self.head.heading() != LEFT:
            self.head.setheading(RIGHT)
