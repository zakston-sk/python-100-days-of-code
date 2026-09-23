"""Snake Game — Part 1 (Day 20).

Creates a snake and lets the player move it with the arrow keys.
"""

from time import sleep
from turtle import Screen

from snake import Snake

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = "LightSlateBlue"
FRAME_DELAY = 0.1  # seconds between frames


def main() -> None:
    """Set up the screen, create the snake, and run the game loop."""
    screen = Screen()
    screen.setup(SCREEN_WIDTH, SCREEN_HEIGHT)
    screen.bgcolor(BACKGROUND_COLOR)
    screen.title("Snake Game — Part 1")
    screen.tracer(0)  # disable automatic animation

    snake = Snake()

    screen.onkey(snake.up, "Up")
    screen.onkey(snake.down, "Down")
    screen.onkey(snake.left, "Left")
    screen.onkey(snake.right, "Right")
    screen.listen()

    while True:
        screen.update()
        sleep(FRAME_DELAY)
        snake.move()


if __name__ == "__main__":
    main()
