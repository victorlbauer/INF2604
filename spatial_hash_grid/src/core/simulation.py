import os
import random

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

from dataclasses import dataclass

from .particles import Particle
from .colors import BLACK
from .collision import create_collision_strategy

@dataclass
class Settings:
    # Particles
    MIN_PARTICLES: int = 10
    MAX_PARTICLES: int = 500
    MIN_RADIUS: int = 5
    MAX_RADIUS: int = 20
    MIN_VELOCITY: int = 50
    MAX_VELOCTY: int = 300

    # Collision
    DEFAULT_STRATEGY: str = "naive"

    # Window
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600


class Simulation:
    def __init__(self, n: int, r: int, v: int, s: str=None):
        self._settings = Settings()

        n = n if n is not None else self._settings.MIN_PARTICLES
        r = r if r is not None else self._settings.MIN_RADIUS
        v = v if v is not None else self._settings.MIN_VELOCITY
        s = s if s is not None else self._settings.DEFAULT_STRATEGY

        self._n = max(self._settings.MIN_PARTICLES, min(n, self._settings.MAX_PARTICLES))
        self._r = max(self._settings.MIN_RADIUS, min(r, self._settings.MAX_RADIUS))
        self._v = max(self._settings.MIN_VELOCITY, min(v, self._settings.MAX_VELOCTY))

        self._collision_strategy = create_collision_strategy(s, r)

        self.__init_pygame()
        self.__setup()
        self.__run()

    def __init_pygame(self):
        pygame.init()
        self._screen = pygame.display.set_mode((self._settings.WINDOW_WIDTH, self._settings.WINDOW_HEIGHT))
        self._clock = pygame.time.Clock()

    def __setup(self):
        width  = self._settings.WINDOW_WIDTH
        height = self._settings.WINDOW_HEIGHT
        offset = 20

        # Create particles
        self._particles = []
        for _ in range(self._n):
            x = random.randint(offset, width - offset)
            y = random.randint(offset, height - offset)
            self._particles.append(Particle(x, y, self._r, self._v, (width, height)))

    def __run(self):
        self._running = True

        while self._running:
            dt = self._clock.tick() / 1000
            self.__poll_events()
            self.__update(dt)
            self.__render()

    def __poll_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
    
    def __update(self, dt: float):
        for p in self._particles:   
            p.update(dt)

        self._collision_strategy.execute(self._particles)

        pygame.display.set_caption(f"Spatial Hash Grid Demo - FPS: {self._clock.get_fps():.2f}")

    def __render(self):
        self._screen.fill(BLACK)

        for p in self._particles:
            pygame.draw.circle(self._screen, p.color, (p.x, p.y), p.r)

        pygame.display.flip()