"""Keyboard input manager for the Pong game (Day 22)."""

from turtle import _Screen

_BINDINGS = {
    "left_up": ["w", "W"],
    "left_down": ["s", "S"],
    "right_up": ["Up"],
    "right_down": ["Down"],
    "pause": ["space"],
    "quit": ["q", "Q"],
    "restart": ["r", "R"],
}

_DISCRETE_ACTIONS = {"pause", "quit", "restart"}


class InputManager:
    """Tracks currently held keys and one-shot key presses."""

    def __init__(self, screen: _Screen) -> None:
        self._screen = screen
        self._held: set[str] = set()
        self._pending: set[str] = set()
        self._bind()

    def _bind(self) -> None:
        """Register press and release handlers for every action."""
        self._screen.listen()
        for action, keysyms in _BINDINGS.items():
            for keysym in keysyms:
                self._screen.onkeypress(
                    self._make_handler(action, pressed=True), keysym
                )
                self._screen.onkey(self._make_handler(action, pressed=False), keysym)

    def _make_handler(self, action: str, pressed: bool):
        """Return a callback that presses or releases the given action."""

        def _handler() -> None:
            self._press(action) if pressed else self._release(action)

        return _handler

    def _press(self, action: str) -> None:
        """Mark an action as held; queue one-shot actions once per press."""
        if action in _DISCRETE_ACTIONS and action not in self._held:
            self._pending.add(action)
        self._held.add(action)

    def _release(self, action: str) -> None:
        """Mark an action as no longer held."""
        self._held.discard(action)

    def is_active(self, action: str) -> bool:
        """Return True if the action is currently held."""
        return action in self._held

    def consume_pressed(self, action: str) -> bool:
        """Return True exactly once per discrete press."""
        if action in self._pending:
            self._pending.discard(action)
            return True
        return False
