"""Heads-up display for the Turtle Crossing game (Day 23)."""

from turtle import Turtle

import settings


class Hud:
    """Displays the level counter and status messages."""

    def __init__(self) -> None:
        self._level_writer = self._build_writer()
        self._message_writer = self._build_writer()
        self.set_level(1)

    def set_level(self, level: int) -> None:
        """Redraw the level counter in the top-left corner."""
        self._level_writer.clear()
        self._level_writer.goto(settings.HUD_LEVEL_POSITION)
        self._level_writer.write(
            f"Level: {level}",
            font=settings.HUD_FONT,
        )

    def show_message(self, text: str) -> None:
        """Display a centred status message (e.g. game over, paused)."""
        self._message_writer.clear()
        self._message_writer.goto(settings.HUD_MESSAGE_POSITION)
        self._message_writer.write(
            text,
            align="center",
            font=settings.HUD_MESSAGE_FONT,
        )

    def clear_message(self) -> None:
        """Remove the current status message."""
        self._message_writer.clear()

    @staticmethod
    def _build_writer() -> Turtle:
        """Return a hidden, pen-up turtle ready for writing."""
        writer = Turtle()
        writer.hideturtle()
        writer.penup()
        writer.color(settings.HUD_COLOR)
        return writer
