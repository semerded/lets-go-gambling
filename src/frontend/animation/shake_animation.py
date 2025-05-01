import pygame as pg
import math
from src.frontend.animation.animation import Animation

class ShakeAnimation(Animation):
    def __init__(self, intensity: int = 10, frequency: float = 1.5, duration: float = 0.5):
        super().__init__()
        self.intensity = intensity
        self.frequency = frequency  # Hz (cycles per second)
        self.duration = duration
        self.start_time = pg.time.get_ticks()
        self.busy = True

    def animate(self, surface: pg.Surface, rect: pg.Rect) -> tuple:
        current_time = pg.time.get_ticks()
        elapsed_time = (current_time - self.start_time) / 1000

        if self.duration != -1 and elapsed_time >= self.duration:
            self.busy = False
            return surface, rect

        # Use smooth sine/cosine shake
        angle = 2 * math.pi * self.frequency * elapsed_time
        offset_x = int(math.sin(angle) * self.intensity)
        offset_y = int(math.cos(angle) * self.intensity * 0.5)

        shaken_rect = rect.copy()
        shaken_rect.centerx += offset_x
        shaken_rect.centery += offset_y

        return surface, shaken_rect
