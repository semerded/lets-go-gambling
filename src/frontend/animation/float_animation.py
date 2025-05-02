import pygame as pg
import math
from src.frontend.animation.animation import Animation
from random import uniform

class FloatAnimation(Animation):
    def __init__(self, radius: int = 25, duration: float = -1, k: float = 0):
        super().__init__()
        self.radius = radius
        self.duration = duration
        self.x_sin = EasedSine(k)
        self.y_sin = EasedSine(k)
        self.start_time = pg.time.get_ticks()
        self.busy = True
        self.rect = None
        self.stopping = False
        self.original_radius = radius

    def animate(self, surface: pg.Surface, rect: pg.Rect) -> tuple:
        current_time = pg.time.get_ticks()
        elapsed_time = (current_time - self.start_time) / 1000

        if self.duration != -1 and elapsed_time >= self.duration:
            self.busy = False
            return surface, rect

        offset_x = self.x_sin.update() * self.radius
        offset_y = self.y_sin.update() * self.radius

        if self.rect is None:
            self.rect = rect.copy()

        # Update position based on the offset
        rect.centerx = self.rect.centerx + offset_x
        rect.centery = self.rect.centery + offset_y

        if self.stopping and self.x_sin.is_reset() and self.y_sin.is_reset():
            self.busy = False

        return surface, rect

    def stop(self):
        self.stopping = True
        self.x_sin.prepare_to_reset()
        self.y_sin.prepare_to_reset()

    def set_speed_and_intensity(self, speed_range: tuple[float, float], radius: int, k: float):
        self.radius = radius
        self.x_sin.set_speed_range(*speed_range)
        self.y_sin.set_speed_range(*speed_range)
        self.x_sin.k = k
        self.y_sin.k = k

class EasedSine:
    def __init__(self, smoothness: float = 1):
        self.sin_going_up = True
        self.angle = 0
        self.k = smoothness
        self.speed_range = (0.005, 0.02)
        self.resetting = False

    def eased_sine(self, x: float) -> float:
        return (0.5 + math.sin(x * math.pi - math.pi / 2) / 2) ** ((2 * (1 - x)) ** self.k)

    def update(self):
        speed = uniform(*self.speed_range)
        if self.sin_going_up:
            self.angle += speed
            if self.angle >= 1:
                self.angle = 1
                self.sin_going_up = False
        else:
            self.angle -= speed
            if self.angle <= 0:
                self.angle = 0
                self.sin_going_up = True

        if self.resetting and self.angle == 0:
            self.resetting = False

        return self.eased_sine(self.angle)

    def prepare_to_reset(self):
        self.resetting = True

    def is_reset(self):
        return self.angle == 0 and not self.resetting

    def set_speed_range(self, low: float, high: float):
        self.speed_range = (low, high)
