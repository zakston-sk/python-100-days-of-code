"""Ball for the Pong game (Day 22).

The ball moves using delta-time physics and bounces off walls and paddles.
Paddle bounces use an angle proportional to the hit offset, which gives
the player directional control.
"""

from math import cos, hypot, radians, sin
from random import uniform
from turtle import Turtle

import settings


class Ball(Turtle):
    """A moving ball with angle-based bouncing physics."""

    def __init__(self) -> None:
        super().__init__(shape="circle")
        self.color(settings.BALL_COLOR)
        self.shapesize(
            stretch_wid=settings.BALL_SIZE,
            stretch_len=settings.BALL_SIZE,
        )
        self.penup()
        self.speed(0)
        self.x_speed = settings.BALL_INITIAL_SPEED_X
        self.y_speed = settings.BALL_INITIAL_SPEED_Y

    def move(self, dt: float) -> None:
        """Move the ball by its velocity scaled by delta time."""
        new_x = self.xcor() + self.x_speed * dt
        new_y = self.ycor() + self.y_speed * dt
        self.goto(new_x, new_y)

    def speed_magnitude(self) -> float:
        """Return the current speed (magnitude of the velocity vector)."""
        return hypot(self.x_speed, self.y_speed)

    def bounce_off_wall(self) -> None:
        """Reverse the vertical component of the velocity."""
        self.y_speed *= -1

    def bounce_off_paddle(self, hit_offset: float) -> None:
        """Bounce off a paddle, using hit_offset to steer the ball.

        Args:
            hit_offset: A value in [-1.0, 1.0]. Negative means the ball hit
                the lower half of the paddle, positive means the upper half.
        """
        speed = min(
            self.speed_magnitude() * settings.BALL_SPEEDUP_FACTOR,
            settings.BALL_MAX_SPEED,
        )
        angle = hit_offset * radians(settings.BALL_MAX_BOUNCE_ANGLE_DEG)
        direction = 1 if self.x_speed > 0 else -1
        self.x_speed = -direction * speed * cos(angle)
        self.y_speed = speed * sin(angle)

    def reset_position(self, direction: int = 1) -> None:
        """Move the ball to the centre and serve it in the given direction.

        Args:
            direction: 1 to serve to the right, -1 to serve to the left.
        """
        self.goto(0, 0)
        speed = hypot(
            settings.BALL_INITIAL_SPEED_X,
            settings.BALL_INITIAL_SPEED_Y,
        )
        angle = radians(
            uniform(
                -settings.BALL_SERVE_ANGLE_DEG,
                settings.BALL_SERVE_ANGLE_DEG,
            )
        )
        self.x_speed = direction * speed * cos(angle)
        self.y_speed = speed * sin(angle)
