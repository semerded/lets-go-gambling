import pygame as pg
from src.frontend.animation.move_animation import MoveAnimation
from src.frontend.animation.fade_animation import FadeAnimation
import gFrame as gf
from src import data

class MovingFadingText:
    def __init__(self, text, color, duration, start_pos, end_pos):
        self.text = text
        self.color = color
        self.duration = duration
        self.start_pos = start_pos
        self.end_pos = end_pos
        
        font = gf.Font.customFont(int(gf.ScreenUnit.vw(4)), "assets/font/CasinoShadow.ttf")
        self.surface = font.render(f"- {self.text}", True, self.color)
        self.rect: pg.Rect = self.surface.get_rect()
        self.rect.x = start_pos[0]
        self.rect.y = start_pos[1]
        self.move_animation = MoveAnimation(self.start_pos, self.end_pos, self.duration)
        self.fade_animation = FadeAnimation(self.surface, self.duration, "in-out", "ease-out")
        
    def draw(self):
        if not self.move_animation.is_done():
            self.surface, self.rect = self.move_animation.animate(self.surface, self.rect)
            self.surface, self.rect = self.fade_animation.animate(self.surface, self.rect)
            data.APP_SURFACE.blit(self.surface, self.rect)