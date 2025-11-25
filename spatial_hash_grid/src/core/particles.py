import math
import random

from typing import Tuple

from .colors import WHITE

class Particle:
    def __init__(self, x: float, y: float, r: int, v: int, max_dist: Tuple[int, int]):
        self.x = x
        self.y = y
        self.r = r
        self.v = v

        self.color = WHITE

        angle = random.uniform(0, 2 * math.pi)
        self._dx = math.cos(angle)
        self._dy = math.sin(angle)
        
        self._max_dist = max_dist

    def update(self, dt: float):
        def bounce(pos, direction, min_val, max_val):
            if pos < min_val:
                return min_val, -direction
            if pos > max_val:
                return max_val, -direction
            return pos, direction

        self.x += self.v * self._dx * dt
        self.y += self.v * self._dy * dt

        self.x, self._dx = bounce(self.x, self._dx, self.r, self._max_dist[0] - self.r)
        self.y, self._dy = bounce(self.y, self._dy, self.r, self._max_dist[1] - self.r)