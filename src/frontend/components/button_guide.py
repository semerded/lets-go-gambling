import pygame as pg
import gFrame as gf
from src import data
from src.frontend.pages.blackjack.components.rounded_surface_corners import round_corners

class ButtonGuide():
    def __init__(self, hit = None, stand = None, a = None, b = None, x = None, y = None):
        self.hit = hit
        self.stand = stand
        self.a = a
        self.b = b
        self.x = x
        self.y = y
        
        self.rect = gf.Rect(gf.ScreenUnit.vw(60), 0, gf.ScreenUnit.vw(40), gf.ScreenUnit.vh(20))
        self.bg_surface = pg.Surface((self.rect.w, self.rect.h), pg.SRCALPHA)
        self.bg_surface.fill((0, 0, 0, 40))
        self.bg_surface = round_corners(self.bg_surface, int(gf.ScreenUnit.vw(1)))
        
       
        
        font = gf.Font.customFont(int(gf.ScreenUnit.vw(2)))
        self.hit_button = gf.Button((self.rect.rw(30), self.rect.rh(30)), gf.Color.WHITE, 8)
        if hit is not None:
            self.hit_button.text(hit, font, gf.Color.DARKMODE)
        self.stand_button = gf.Button((self.rect.rw(30), self.rect.rh(30)), gf.Color.WHITE, 8)
        if stand is not None:
            self.stand_button.text(stand, font, gf.Color.DARKMODE)
        self.a_button = gf.Button((self.rect.rw(30), self.rect.rh(30)), gf.Color.GREEN, 8)
        if a is not None:
            self.a_button.text(a, font, gf.Color.DARKMODE)
            
        self.b_button = gf.Button((self.rect.rw(30), self.rect.rh(30)), gf.Color.RED, 8)
        if b is not None:
            self.b_button.text(b, font, gf.Color.DARKMODE)
        
        self.x_button = gf.Button((self.rect.rw(30), self.rect.rh(30)), gf.Color.BLUE, 8)
        if x is not None:
            self.x_button.text(x, font, gf.Color.DARKMODE)
            
        self.y_button = gf.Button((self.rect.rw(30), self.rect.rh(30)), gf.Color.YELLOW, 8)
        if y is not None:
            self.y_button.text(y, font, gf.Color.DARKMODE)            
        
    def draw(self):
        data.APP_SURFACE.blit(self.bg_surface, self.rect)
        self.hit_button.place(self.rect.pw(3), self.rect.ph(3))
        self.stand_button.place(self.rect.pw(3), self.rect.ph(67))
        self.a_button.place(self.rect.pw(53), self.rect.ph(67))
        self.b_button.place(self.rect.pw(67), self.rect.ph(35))
        self.x_button.place(self.rect.pw(35), self.rect.ph(35))
        self.y_button.place(self.rect.pw(53), self.rect.ph(3))