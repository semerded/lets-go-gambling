import pygame as pg
from src.screen.animation.animation import Animation

class MoveAnimation(Animation):
    def __init__(self, start_pos, end_pos, duration):
        super().__init__()
        self.start_pos = pg.Vector2(start_pos)
        self.end_pos = pg.Vector2(end_pos)
        self.duration = duration
        self.elapsed = 0.0
        
        self.start_time = pg.time.get_ticks()  # Record the start time


        
    def animate(self, surface: pg.Surface, rect: pg.Rect):
        current_time = pg.time.get_ticks()
        delta_time = (current_time - self.start_time) / 1000  # Convert to seconds

        t = min(delta_time / self.duration, 1)  # Normalize between 0 and 1
        rect.topleft = self.start_pos.lerp(self.end_pos, t)
        if t >= 1:
            self.busy = False
            t = 1

        return surface, rect