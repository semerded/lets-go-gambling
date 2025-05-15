import pygame as pg
import gFrame as gf
from src import data

class ButtonGuide():
    def __init__(self, hit = None, stand = None, a = None, b = None, x = None, y = None):
        self.hit = hit
        self.stand = stand
        self.a = a
        self.b = b
        self.x = x
        self.y = y
        
        self.rect = gf.Rect(gf.ScreenUnit.vw(60), 0, gf.ScreenUnit.vw(40), gf.ScreenUnit.vh(25))
        
        font = gf.Font.customFont(int(gf.ScreenUnit.vw(2)))
        if hit is not None:
            self.hit_button = gf.Button((self.rect.rw(30), self.rect.rh(30)), gf.Color.WHITE, 8)
            self.hit_button.text(hit, font, gf.Color.DARKMODE)
        if stand is not None:
            self.stand_button = gf.Button((self.rect.rw(30), self.rect.rh(30)), gf.Color.WHITE, 8)
            self.stand_button.text(stand, font, gf.Color.DARKMODE)
        if a is not None:
            self.a_button = gf.Button((self.rect.rw(30), self.rect.rh(30)), gf.Color.GREEN, 8)
            self.a_button.text(a, font, gf.Color.DARKMODE)
            
        if b is not None:
            self.b_button = gf.Button((self.rect.rw(30), self.rect.rh(30)), gf.Color.RED, 8)
            self.b_button.text(b, font, gf.Color.DARKMODE)
        
        if x is not None:
            self.x_button = gf.Button((self.rect.rw(30), self.rect.rh(30)), gf.Color.BLUE, 8)
            self.x_button.text(x, font, gf.Color.DARKMODE)
            
        if y is not None:
            self.y_button = gf.Button((self.rect.rw(30), self.rect.rh(30)), gf.Color.YELLOW, 8)
            self.y_button.text(y, font, gf.Color.DARKMODE)            
        
    def draw(self):
        if self.hit is not None:
            self.hit_button.place(self.rect.pw(3), self.rect.ph(3))
        if self.stand is not None:
            self.stand_button.place(self.rect.pw(3), self.rect.ph(67))
        if self.a is not None:
            self.a_button.place(self.rect.pw(53), self.rect.ph(67))
        if self.b is not None:
            self.b_button.place(self.rect.pw(67), self.rect.ph(35))
        if self.x is not None:
            self.x_button.place(self.rect.pw(35), self.rect.ph(35))
        if self.y is not None:
            self.y_button.place(self.rect.pw(53), self.rect.ph(3))