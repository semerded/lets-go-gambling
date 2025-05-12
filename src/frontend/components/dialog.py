from typing import Callable
from src.frontend.components.textbox import TextBox
import gFrame as gf
import pygame as pg
from src import data

class Dialog:
    dialog_rect: gf.Rect = gf.Rect(gf.ScreenUnit.vw(15), gf.ScreenUnit.vh(20), gf.ScreenUnit.vw(70), gf.ScreenUnit.vh(60))
    def __init__(self, text: str, on_accept: Callable ,on_cancel: Callable):
        self.surface = pg.Surface((self.dialog_rect.w, self.dialog_rect.h))
        self.text = TextBox(self.dialog_rect.pw(5), self.dialog_rect.ph(5), self.dialog_rect.rw(90), gf.Font.H2, gf.Color.WHITE)
        self.text.set_text(text)
        
        self.accept_button = gf.Button((self.dialog_rect.rw(40), self.dialog_rect.rh(10)), gf.Color.SPRING_GREEN, 8)
        self.accept_button.text("Accept [A]", gf.Font.XLARGE, gf.Color.DARKMODE)
        self.cancel_button = gf.Button((self.dialog_rect.rw(40), self.dialog_rect.rh(10)), gf.Color.LAVA_RED, 8)
        self.cancel_button.text("Cancel [B]", gf.Font.XLARGE, gf.Color.DARKMODE)
        
        self.on_accept = on_accept
        self.on_cancel = on_cancel
    
    def draw(self):
        self.surface.fill(gf.Color.DARK_GRAY, self.dialog_rect)
        self.text.draw(self.surface)
        self.accept_button.place(self.dialog_rect.pw(5), self.dialog_rect.ph(80))
        self.cancel_button.place(self.dialog_rect.pw(55), self.dialog_rect.ph(80))
        