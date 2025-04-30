import pygame as pg
import math
from src.frontend.animation.animation import Animation

class FlipAnimation(Animation):
    def __init__(self, front_surface: pg.Surface, back_surface: pg.Surface, front_to_back: bool = True, duration: float = 0.5):
        super().__init__()
        self.front_surface = front_surface
        self.back_surface = back_surface
        self.flipping_forward = front_to_back
        self.duration = duration  # duration of the flip in seconds
        self.start_time = pg.time.get_ticks()
        self.busy = True

    def animate(self, surface: pg.Surface, rect: pg.Rect) -> tuple:
        current_time = pg.time.get_ticks()
        elapsed_time = (current_time - self.start_time) / 1000
        t = min(elapsed_time / self.duration, 1.0)

        # Flip angle in degrees from 0 to 180 (or reverse)
        angle = (1 - t) * 180 if self.flipping_forward else t * 180
        radians = math.radians(angle)
        scale_x = abs(math.cos(radians))

        # Avoid scale of 0
        scale_x = max(scale_x, 0.01)

        # Choose which side of the flip to show
        if angle < 90:
            source = self.front_surface
        else:
            source = self.back_surface

        # Apply Y-axis-like flip effect via horizontal scaling
        new_width = max(1, int(source.get_width() * scale_x))
        scaled_surface = pg.transform.smoothscale(source, (new_width, source.get_height()))
        new_rect = scaled_surface.get_rect(center=rect.center)

        if t >= 1.0:
            self.busy = False

        return scaled_surface, new_rect
