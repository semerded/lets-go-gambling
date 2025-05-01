import pygame as pg
from src.frontend.animation.animation import Animation

class RotateAnimation(Animation):
    def __init__(self, rect: pg.Rect, end_angle: float, start_angle: float = 0, duration: float = 0.5):
        super().__init__()
        self.original_rect = rect.copy()
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.duration = duration
        self.start_time = pg.time.get_ticks()
        self.busy = True

    def animate(self, surface: pg.Surface, rect: pg.Rect) -> tuple:
        current_time = pg.time.get_ticks()
        elapsed_time = (current_time - self.start_time) / 1000
        progress = min(elapsed_time / self.duration, 1.0)

        if progress >= 1.0:
            self.busy = False

        angle = self.start_angle + (self.end_angle - self.start_angle) * progress
        rotated_surface = pg.transform.rotozoom(surface, -angle, 1.0)
        new_rect = rotated_surface.get_rect(center=self.original_rect.center)

        return rotated_surface, new_rect

    def reset(self):
        self.start_time = pg.time.get_ticks()
        self.busy = True
