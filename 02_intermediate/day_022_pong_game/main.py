"""Entry point for the Pong game (Day 22)."""

from game import PongGame


def main() -> None:
    """Create and run the Pong game."""
    game = PongGame()
    game.run()


if __name__ == "__main__":
    main()
