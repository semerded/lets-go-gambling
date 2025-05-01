import pygame as pg
import math
from src.frontend.animation.animation import Animation
from random import uniform

class FloatAnimation(Animation):
    def __init__(self, radius: int = 25, duration: float = -1, k: float = 0):
        super().__init__()
        self.radius = radius  # Max displacement of 10px (up and down)
        self.duration = duration
        self.x_sin = EasedSine(k)
        self.y_sin = EasedSine(k)
        self.start_time = pg.time.get_ticks()
        self.busy = True
        self.rect = None

    def animate(self, surface: pg.Surface, rect: pg.Rect) -> tuple:
        # Calculate the elapsed time since the animation started
        current_time = pg.time.get_ticks()
        elapsed_time = (current_time - self.start_time) / 1000

        # Stop animation after duration if it's set
        if self.duration != -1 and elapsed_time >= self.duration:
            self.busy = False
            return surface, rect

        # Normalize time for easing (0 to 1)

        # Apply the eased sine formula directly to the progress

        # Increase the angle continuously for smooth sine wave movement
        

        # Calculate the offset using the eased value (sine wave oscillation)
        offset_x = self.x_sin.update() * self.radius 
        offset_y = self.y_sin.update() * self.radius 
        

        if self.rect is None:
            self.rect = rect.copy()
            
            
            

        # Update position based on the offset
        rect.centerx = self.rect.centerx + offset_x
        rect.centery = self.rect.centery + offset_y

        return surface, rect

class EasedSine:
    def __init__(self, smoothness: float = 1):
        self.sin_going_up = True
        self.angle = 0
        self.k = smoothness
        
    def eased_sine(self, x: float) -> float:
        return (0.5 + math.sin(x * math.pi - math.pi / 2) / 2) ** ((2 * (1 - x)) ** self.k)
    
    def update(self):
        if self.sin_going_up:
            self.angle += uniform(0.005, 0.02)
            if self.angle >= 1:
                self.sin_going_up = False
                self.angle = 1
        else:
            self.angle -= uniform(0.005, 0.02)
            if self.angle <= 0:
                self.sin_going_up = True
                self.angle = 0
        return self.eased_sine(self.angle)
