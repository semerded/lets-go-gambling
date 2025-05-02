import pygame as pg
from src.frontend.animation.animation import Animation

class RotateAnimation(Animation):
    def __init__(self, rect: pg.Rect, end_angle: float, start_angle: float = 0, duration: float = 0.5):
        super().__init__()
        self.original_rect = rect.copy()
        self.surface = None
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.duration = duration
        self.start_time = pg.time.get_ticks()
        self.busy = True
        
    def animate(self, surface: pg.Surface, rect: pg.Rect) -> tuple:
        if self.surface == None:
            self.surface = surface.copy()
        current_time = pg.time.get_ticks()
        elapsed_time = (current_time - self.start_time) / 1000  # Calculate elapsed time in seconds

        # Calculate the progress (t) of the animation
        t = min(elapsed_time / self.duration, 1.0)
        
        if t >= 1.0:
            self.busy = False
            t = 1

        # Determine the current angle of the flip based on the direction and progress
        # if self.rotating_clockwise:
        angle = self.start_angle + (self.end_angle - self.start_angle) * t
        # else:
        #     angle = 180 * t  # From 0 to 180

        
        new_surface = pg.transform.rotozoom(self.surface, angle, 1)
        new_rect = new_surface.get_rect(center=rect.center)
        
        return new_surface, new_rect

    def reset(self):
        # Reset the animation start time and set it as busy again
        self.start_time = pg.time.get_ticks()
        self.busy = True

    def get_current_angle(self):
        # Return the current angle based on the elapsed time and progress
        current_time = pg.time.get_ticks()
        elapsed_time = (current_time - self.start_time) / 1000
        progress = min(elapsed_time / self.duration, 1.0)
        return self.start_angle + (self.end_angle - self.start_angle) * progress
