import math

from itertools import combinations
from collections import defaultdict
from abc import ABC, abstractmethod

from .colors import WHITE, RED
from .particles import Particle

class CollisionStrategy(ABC):
    @abstractmethod
    def execute(self):
        pass


class NaiveStrategy(CollisionStrategy):
    def __init__(self):
        super().__init__()

    def execute(self, particles: list[Particle]):
        # Reset color
        for p in particles:
            p.color = WHITE

        # Check for collisions against every other particle
        for p1, p2 in combinations(particles, 2):
            dx = p1.x - p2.x
            dy = p1.y - p2.y
            dist = math.hypot(dx, dy)

            if dist < p1.r + p2.r:
                p1.color = RED
                p2.color = RED


class SpatialHashGrid:
    def __init__(self, cell_size):
        self._cell_size = cell_size
        self._cells = defaultdict(list)
    
    def add(self, particle: Particle):
        r = particle.r

        min_x, min_y = self.__hash(particle.x - r, particle.y - r)
        max_x, max_y = self.__hash(particle.x + r, particle.y + r)

        for cx in range(min_x, max_x + 1):
            for cy in range(min_y, max_y + 1):
                self._cells[(cx, cy)].append(particle)

    def all_cell_groups(self):
        return self._cells.values()

    def clear(self):
        self._cells.clear()

    def __hash(self, x: float, y: float):
        return int(x // self._cell_size), int(y // self._cell_size)


class SGHStrategy(CollisionStrategy):
    def __init__(self, radius: float):
        super().__init__()

        # Use particle's radius as heuristic
        self._grid = SpatialHashGrid(2 * radius)

    def execute(self, particles: list[Particle]):
        self._grid.clear()

        for p in particles:
            p.color = WHITE
            self._grid.add(p)

        for cell_particles in self._grid.all_cell_groups():
            if len(cell_particles) < 2:
                continue

            # Check for collisions against every other particle within the same cell
            for p1, p2 in combinations(cell_particles, 2):
                dx = p1.x - p2.x
                dy = p1.y - p2.y
                dist = math.hypot(dx, dy)

                if dist < p1.r + p2.r:
                    p1.color = RED
                    p2.color = RED


def create_collision_strategy(strategy: str, radius: int):
    match(strategy):
        case "naive":
            return NaiveStrategy()
        case "shg":
            return SGHStrategy(radius)
        case _:
            raise ValueError(f"Invalid collision strategy: {strategy}")