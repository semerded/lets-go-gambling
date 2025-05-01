import pygame as pg
from src.frontend.animation.animation import Animation

class ScaleAnimation(Animation):
    def __init__(self, rect: pg.Rect, end_scale: float, start_scale: float = 100, duration: float = 0.5):
        super().__init__()
        self.original_rect = rect.copy()
        self.start_scale = start_scale / 100.0
        self.end_scale = end_scale / 100.0
        self.duration = duration
        self.start_time = pg.time.get_ticks()
        self.busy = True

    def animate(self, surface: pg.Surface, rect: pg.Rect) -> tuple:
        current_time = pg.time.get_ticks()
        elapsed_time = (current_time - self.start_time) / 1000
        progress = min(elapsed_time / self.duration, 1.0)

        if progress >= 1.0:
            self.busy = False

        scale = self.start_scale + (self.end_scale - self.start_scale) * progress
        new_width = int(self.original_rect.width * scale)
        new_height = int(self.original_rect.height * scale)

        scaled_surface = pg.transform.smoothscale(surface, (new_width, new_height))
        new_rect = scaled_surface.get_rect(center=self.original_rect.center)

        return scaled_surface, new_rect

    def reset(self):
        self.start_time = pg.time.get_ticks()
        self.busy = True

    def get_current_scale(self) -> float:
        current_time = pg.time.get_ticks()
        elapsed_time = (current_time - self.start_time) / 1000
        progress = min(elapsed_time / self.duration, 1.0)
        return self.start_scale + (self.end_scale - self.start_scale) * progress