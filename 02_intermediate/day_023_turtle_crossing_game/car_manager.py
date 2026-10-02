"""Car spawning, recycling, and traffic density (Day 23)."""

from random import choice, uniform

from car import Car

import settings


class CarManager:
    """Manages spawning, moving, and recycling cars.

    Higher levels shrink the spawn delay range, increasing traffic density.
    Off-screen cars are moved into a reuse pool instead of being destroyed.
    """

    def __init__(self) -> None:
        self.cars: list[Car] = []
        self._pool: list[Car] = []
        self._level = 1
        self._spawn_timer = 0.0
        self._next_spawn_delay = self._random_spawn_delay()

    def set_level(self, level: int) -> None:
        """Set the traffic density level."""
        self._level = level

    def reset(self, level: int = 1) -> None:
        """Clear active traffic and restart spawning at the given level."""
        for car in self.cars:
            car.hideturtle()
        self._pool.extend(self.cars)
        self.cars = []
        self._level = level
        self._spawn_timer = 0.0
        self._next_spawn_delay = self._random_spawn_delay()

    def update(self, dt: float) -> None:
        """Move cars, recycle off-screen ones, and spawn new cars over time."""
        self._recycle_offscreen_cars()
        for car in self.cars:
            car.update(dt)

        self._spawn_timer += dt
        if self._spawn_timer >= self._next_spawn_delay:
            self._spawn_timer = 0.0
            self._next_spawn_delay = self._random_spawn_delay()
            self._spawn_car()

    def _spawn_car(self) -> None:
        """Spawn a car at the right edge in a random lane."""
        lanes = range(
            int(settings.CAR_MANAGER_MIN_CAR_START_POSITION_Y),
            int(settings.CAR_MANAGER_MAX_CAR_START_POSITION_Y) + 1,
            20,
        )
        position = (settings.CAR_MANAGER_CAR_START_POSITION_X, choice(lanes))
        if self._pool:
            car = self._pool.pop()
            car.respawn(position)
        else:
            car = Car(position)
        self.cars.append(car)

    def _recycle_offscreen_cars(self) -> None:
        """Move cars that have fully left the screen into the reuse pool."""
        offscreen_x = -settings.SCREEN_W / 2 - settings.CAR_W
        still_active = []
        for car in self.cars:
            if car.xcor() < offscreen_x:
                car.hideturtle()
                self._pool.append(car)
            else:
                still_active.append(car)
        self.cars = still_active

    def _random_spawn_delay(self) -> float:
        """Return a random spawn delay for the current level."""
        min_delay, max_delay = self._spawn_delay_range()
        return uniform(min_delay, max_delay)

    def _spawn_delay_range(self) -> tuple[float, float]:
        """Return the current (min, max) spawn delay range."""
        factor = settings.CAR_MANAGER_LEVEL_SPAWN_DECAY ** (self._level - 1)
        min_delay = max(
            settings.CAR_MANAGER_MIN_SPAWN_DELAY * factor,
            settings.CAR_MANAGER_SPAWN_DELAY_FLOOR,
        )
        max_delay = max(
            settings.CAR_MANAGER_MAX_SPAWN_DELAY * factor,
            min_delay + 0.05,
        )
        return min_delay, max_delay
