from src import data
import gFrame as gf
import pygame as pg
from random import randint

x_pos_bound = int(gf.ScreenUnit.vw(100) - data.POKER_CHIPS[0].get_rect().width)
y_pos_start = int(0 - data.POKER_CHIPS[0].get_rect().height)

class FallingChip:
    def __init__(self):
        self.image: pg.Surface = data.POKER_CHIPS[randint(0, len(data.POKER_CHIPS) - 1)]
        self.x_pos = randint(0, x_pos_bound)
        self.y_pos = y_pos_start
        self.speed = randint(5, 15)
        
    def move(self):
        self.y_pos += self.speed
        
    def place(self):
        data.APP_SURFACE.blit(self.image, (self.x_pos, self.y_pos))
        
    def is_descended_completely_into_the_abyss(self):
        """Checks if the chip has descended to below the screen or not

        Returns:
            bool: if the chip has descended to below the screen
        """
        return self.y_pos > gf.ScreenUnit.vh(100)