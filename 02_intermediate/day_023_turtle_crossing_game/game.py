"""Turtle Crossing game loop (Day 23)."""

from time import perf_counter, sleep
from turtle import Screen, _Screen

import settings
from car_manager import CarManager
from hud import Hud
from player import Player


class Game:
    """Orchestrates the Turtle Crossing game: screen, objects, input, loop."""

    def __init__(self) -> None:
        self.screen: _Screen = self._build_screen()
        self.hud = Hud()
        self.player = Player(settings.PLAYER_START_POSITION)
        self.car_manager = CarManager()
        self.level = 1
        self.is_running = False
        self.is_paused = False
        self.is_game_over = False
        self._bind_keys()

    def run(self) -> None:
        """Run the main game loop."""
        last_time = perf_counter()
        self.is_running = True

        while self.is_running:
            current_time = perf_counter()
            dt = min(current_time - last_time, settings.MAX_DT)
            last_time = current_time

            self._update(dt)

            elapsed = perf_counter() - current_time
            remaining = settings.FRAME_DELAY - elapsed
            if remaining > 0:
                sleep(remaining)

        self.screen.bye()

    def _build_screen(self) -> _Screen:
        """Create and configure the game window."""
        screen = Screen()
        screen.setup(settings.SCREEN_W, settings.SCREEN_H)
        screen.bgcolor(settings.SCREEN_BG)
        screen.title(settings.SCREEN_TITLE)
        screen.tracer(settings.SCREEN_TRACER)
        return screen

    def _bind_keys(self) -> None:
        """Bind all keyboard controls."""
        self.screen.listen()
        self.screen.onkeypress(self._move_up, "Up")
        self.screen.onkeypress(self._move_down, "Down")
        self.screen.onkeypress(self._move_left, "Left")
        self.screen.onkeypress(self._move_right, "Right")
        self.screen.onkeypress(self._quit, "q")
        self.screen.onkeypress(self._toggle_pause, "space")
        self.screen.onkeypress(self._restart, "r")

    def _update(self, dt: float) -> None:
        """Advance the game by one frame."""
        if not self.is_paused and not self.is_game_over:
            self.car_manager.update(dt)
            self._check_state()
        self.screen.update()

    def _check_state(self) -> None:
        """Check win and lose conditions."""
        if self.player.has_finished():
            self._level_up()
        elif self._player_hit_by_car():
            self._trigger_game_over()

    def _player_hit_by_car(self) -> bool:
        """Return True if the player's AABB overlaps any car's AABB."""
        half_player_w = settings.PLAYER_W / 2
        half_player_h = settings.PLAYER_H / 2
        half_car_w = settings.CAR_W / 2
        half_car_h = settings.CAR_H / 2
        px, py = self.player.xcor(), self.player.ycor()
        return any(
            abs(px - car.xcor()) < half_player_w + half_car_w
            and abs(py - car.ycor()) < half_player_h + half_car_h
            for car in self.car_manager.cars
        )

    def _level_up(self) -> None:
        """Increase the level, reset the player, and update the HUD."""
        self.level += 1
        self.car_manager.set_level(self.level)
        self.player.reset()
        self.hud.set_level(self.level)

    def _trigger_game_over(self) -> None:
        """Stop the game and show the game-over message."""
        self.is_game_over = True
        self.hud.show_message("GAME OVER\nR - restart, Q - quit")

    def _move_up(self) -> None:
        """Handle the 'up' key."""
        if not self.is_paused and not self.is_game_over:
            self.player.move_up()

    def _move_down(self) -> None:
        """Handle the 'down' key."""
        if not self.is_paused and not self.is_game_over:
            self.player.move_down()

    def _move_left(self) -> None:
        """Handle the 'left' key."""
        if not self.is_paused and not self.is_game_over:
            self.player.move_left()

    def _move_right(self) -> None:
        """Handle the 'right' key."""
        if not self.is_paused and not self.is_game_over:
            self.player.move_right()

    def _quit(self) -> None:
        """Stop the game loop."""
        self.is_running = False

    def _toggle_pause(self) -> None:
        """Pause or resume the game."""
        if self.is_game_over:
            return
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.hud.show_message("PAUSED")
        else:
            self.hud.clear_message()

    def _restart(self) -> None:
        """Restart the game from level 1."""
        self.level = 1
        self.is_paused = False
        self.is_game_over = False
        self.player.reset()
        self.car_manager.reset(self.level)
        self.hud.set_level(self.level)
        self.hud.clear_message()
