import pygame as pg
from src.frontend.animation.animation import Animation

class FlipAnimation(Animation):
    def __init__(self, front_surface: pg.Surface, back_surface: pg.Surface, front_to_back: bool = True, duration: float = 0.5):
        super().__init__()
        self.front_surface = front_surface
        self.back_surface = back_surface
        self.flipping_forward = front_to_back
        self.duration = duration  # The duration of the flip in seconds
        self.start_time = pg.time.get_ticks()  # Record start time
        self.flip_angle = 180 if front_to_back else 0

    def animate(self, surface: pg.Surface, rect: pg.Rect) -> tuple:
        current_time = pg.time.get_ticks()
        elapsed_time = (current_time - self.start_time) / 1000  # Calculate elapsed time in seconds

        # Calculate the progress (t) of the animation
        t = min(elapsed_time / self.duration, 1.0)

        # Determine the current angle of the flip based on the direction and progress
        if self.flipping_forward:
            self.flip_angle = 180 * (1.0 - t)  # From 180 to 0
        else:
            self.flip_angle = 180 * t  # From 0 to 180

        # Choose the appropriate surface to draw
        if self.flip_angle < 90:
            new_surface = pg.transform.rotate(self.front_surface, self.flip_angle)
        else:
            new_surface = pg.transform.rotate(self.back_surface, self.flip_angle)

        # Correct the position of the rotated surface
        new_rect = new_surface.get_rect(center=rect.center)
        
        if t >= 1.0:
            self.busy = False
            t = 1

        # Return the new surface and rect
        return new_surface, new_rect
