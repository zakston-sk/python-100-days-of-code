"""Pong game loop (Day 22)."""

import time
from turtle import Screen, _Screen

import settings
from ball import Ball
from input_manager import InputManager
from net import Net
from paddle import Paddle
from scoreboard import Scoreboard


class PongGame:
    """Orchestrates the Pong game: screen, objects, input, loop."""

    def __init__(self) -> None:
        self.screen = self._build_screen()
        self.net = Net()
        self.left_paddle = Paddle((-settings.PADDLE_OFFSET_X, 0))
        self.right_paddle = Paddle((settings.PADDLE_OFFSET_X, 0))
        self.ball = Ball()
        self.scoreboard = Scoreboard()
        self.input = InputManager(self.screen)

        self.is_running = False
        self.is_paused = False
        self.is_game_over = False

    def _build_screen(self) -> _Screen:
        """Create and configure the turtle screen."""
        screen = Screen()
        screen.setup(width=settings.SCREEN_WIDTH, height=settings.SCREEN_HEIGHT)
        screen.bgcolor(settings.SCREEN_BG_COLOR)
        screen.title(settings.SCREEN_TITLE)
        screen.tracer(0)
        return screen

    def _toggle_pause(self) -> None:
        """Pause or resume the game."""
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.scoreboard.show_pause()
        else:
            self.scoreboard.update_display()

    def _restart(self) -> None:
        """Restart the game with a fresh score and serve."""
        self.scoreboard.reset()
        self._serve(direction=1)
        self.is_paused = False
        self.is_game_over = False

    def run(self) -> None:
        """Run the main game loop."""
        self.is_running = True
        last_time = time.perf_counter()

        while self.is_running:
            frame_start = time.perf_counter()
            dt = min(frame_start - last_time, settings.MAX_DT)
            last_time = frame_start

            self.screen.update()

            if self.input.consume_pressed("quit"):
                self.is_running = False
                break
            if self.input.consume_pressed("restart"):
                self._restart()
            if self.input.consume_pressed("pause") and not self.is_game_over:
                self._toggle_pause()

            self._apply_paddle_input(dt)

            if not self.is_paused and not self.is_game_over:
                self.ball.move(dt)
                self._handle_wall_collision()
                self._handle_paddle_collision()
                self._handle_scoring()

                winner = self.scoreboard.game_winner()
                if winner:
                    self.is_game_over = True
                    self.scoreboard.show_game_over(winner)

            elapsed = time.perf_counter() - frame_start
            remaining = settings.FRAME_DELAY - elapsed
            if remaining > 0:
                time.sleep(remaining)

        self.screen.bye()

    def _apply_paddle_input(self, dt: float) -> None:
        """Move paddles based on currently held keys."""
        if self.input.is_active("left_up"):
            self.left_paddle.move_up(dt)
        if self.input.is_active("left_down"):
            self.left_paddle.move_down(dt)
        if self.input.is_active("right_up"):
            self.right_paddle.move_up(dt)
        if self.input.is_active("right_down"):
            self.right_paddle.move_down(dt)

    def _handle_wall_collision(self) -> None:
        """Bounce the ball off the top and bottom walls."""
        top = settings.SCREEN_HEIGHT / 2 - settings.BALL_RADIUS
        bottom = -top
        if self.ball.ycor() > top:
            self.ball.goto(self.ball.xcor(), top)
            self.ball.bounce_off_wall()
        elif self.ball.ycor() < bottom:
            self.ball.goto(self.ball.xcor(), bottom)
            self.ball.bounce_off_wall()

    def _handle_paddle_collision(self) -> None:
        """Detect and resolve a collision with either paddle."""
        if self.ball.x_speed > 0 and self._hits_paddle(
            self.right_paddle, from_left=True
        ):
            self._resolve_paddle_hit(self.right_paddle, from_left=True)
        elif self.ball.x_speed < 0 and self._hits_paddle(
            self.left_paddle, from_left=False
        ):
            self._resolve_paddle_hit(self.left_paddle, from_left=False)

    def _resolve_paddle_hit(self, paddle: Paddle, from_left: bool) -> None:
        """Snap the ball to the paddle face and bounce it off."""
        self._snap_ball_to_paddle(paddle, from_left)
        half_h = settings.PADDLE_HALF_HEIGHT
        hit_offset = (self.ball.ycor() - paddle.ycor()) / half_h
        hit_offset = max(-1.0, min(1.0, hit_offset))
        self.ball.bounce_off_paddle(hit_offset)

    def _hits_paddle(self, paddle: Paddle, from_left: bool) -> bool:
        """Return True if the ball overlaps the paddle face."""
        radius = settings.BALL_RADIUS
        half_w = settings.PADDLE_HALF_WIDTH
        half_h = settings.PADDLE_HALF_HEIGHT

        vertical_hit = abs(self.ball.ycor() - paddle.ycor()) <= half_h + radius

        if from_left:
            face_x = paddle.xcor() - half_w
            reached_face = self.ball.xcor() + radius >= face_x
            not_passed_through = self.ball.xcor() <= paddle.xcor() + half_w
        else:
            face_x = paddle.xcor() + half_w
            reached_face = self.ball.xcor() - radius <= face_x
            not_passed_through = self.ball.xcor() >= paddle.xcor() - half_w

        return vertical_hit and reached_face and not_passed_through

    def _snap_ball_to_paddle(self, paddle: Paddle, from_left: bool) -> None:
        """Push the ball just outside the paddle face to avoid overlap."""
        radius = settings.BALL_RADIUS
        half_w = settings.PADDLE_HALF_WIDTH
        if from_left:
            self.ball.goto(paddle.xcor() - half_w - radius, self.ball.ycor())
        else:
            self.ball.goto(paddle.xcor() + half_w + radius, self.ball.ycor())

    def _handle_scoring(self) -> None:
        """Award a point and serve again when the ball passes an edge."""
        right_edge = settings.SCREEN_WIDTH / 2 - settings.BALL_RADIUS
        left_edge = -right_edge

        if self.ball.xcor() > right_edge:
            self.scoreboard.point_left()
            self._serve(direction=-1)
        elif self.ball.xcor() < left_edge:
            self.scoreboard.point_right()
            self._serve(direction=1)

    def _serve(self, direction: int) -> None:
        """Reset the ball and paddles for a new serve."""
        self.ball.reset_position(direction)
        self.left_paddle.reset_position()
        self.right_paddle.reset_position()
