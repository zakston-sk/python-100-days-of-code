"""Snake Game — Part 2 (Day 21)."""

from time import sleep
from turtle import Screen

from food import Food
from scoreboard import Scoreboard
from snake import Snake

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = "LightSlateBlue"
FRAME_DELAY = 0.1

GRID_SIZE = 20
MAX_CELL = 14
BOUNDARY = MAX_CELL * GRID_SIZE
COLLISION_DISTANCE = GRID_SIZE // 2


def main() -> None:
    screen = Screen()
    screen.setup(SCREEN_WIDTH, SCREEN_HEIGHT)
    screen.bgcolor(BACKGROUND_COLOR)
    screen.title("Snake Game — Part 2")
    screen.tracer(0)

    snake = Snake()
    food = Food()
    scoreboard = Scoreboard()

    screen.onkey(snake.up, "Up")
    screen.onkey(snake.down, "Down")
    screen.onkey(snake.left, "Left")
    screen.onkey(snake.right, "Right")
    screen.listen()

    running = True
    while running:
        screen.update()
        sleep(FRAME_DELAY)
        snake.move()

        # Eat food
        if snake.head.distance(food) < COLLISION_DISTANCE:
            food.refresh()
            snake.eat()
            scoreboard.increase_score()

        # Hit the wall
        if (
            snake.head.xcor() > BOUNDARY
            or snake.head.xcor() < -BOUNDARY
            or snake.head.ycor() > BOUNDARY
            or snake.head.ycor() < -BOUNDARY
        ):
            running = False
            scoreboard.game_over()

        # Hit the tail
        for segment in snake.body[1:]:
            if snake.head.distance(segment) < COLLISION_DISTANCE:
                running = False
                scoreboard.game_over()
                break

    screen.exitonclick()


if __name__ == "__main__":
    main()
