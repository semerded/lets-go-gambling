from src.enums import cardType
import gFrame as gf
from src.data import CARD_VALUES
from src import data
import pygame as pg
from src.screen.animation.flip_animation import FlipAnimation
from src.screen.components.rounded_surface_corners import round_corners
from src.screen.animation.move_animation import MoveAnimation

class Card:
    def __init__(self, type: cardType, value: str):
        self.type = type
        self.value = value
        self.rect = gf.Rect(0, 0, *data.CARD_DIMENSIONS)

        self.face_up = False

        self.front = pg.Surface((self.rect.w, self.rect.h), pg.SRCALPHA)
        self._create_front_surface()
        self.back = data.CARD_BACK
        self.current_surface = data.CARD_BACK

        self.animation = None

    def _create_front_surface(self):
        self.front.convert_alpha()       
        img = pg.image.load(f"assets/img/cards/{self.type.name[0].upper()}{self.value}.png").convert_alpha()
        img = pg.transform.scale(img, data.CARD_DIMENSIONS)
        img = round_corners(img, int(gf.ScreenUnit.vw(1)))

        self.front.blit(img, (0, 0))
        
        
    def load_card(self, col, row, card_width, card_height):
        """
        Extract a specific card from the sprite sheet.
        col: column of the card (0-indexed)
        row: row of the card (0-indexed)
        card_width: width of each card
        card_height: height of each card
        """
        rect = pg.Rect(col * card_width, row * card_height, card_width, card_height)

        card = pg.Surface((card_width, card_height), pg.SRCALPHA)
        card.blit(sheet, (0, 0), rect)
        return card
            

    def update(self):
        if self.animation != None:
            if self.animation.is_done():
                self.animation = None
                data.animation_tracker.pop(data.animation_tracker.index(self))
            else:
                self.current_surface, self.rect = self.animation.animate(self.current_surface, self.rect)
        else:
            if self.face_up:
                self.current_surface = self.front
            else:
                self.current_surface = self.back

    def draw(self):
        self.update()  # TODO
        data.APP_SURFACE.blit(self.current_surface, self.rect)

    def flip(self):
        self.face_up = not self.face_up
        self.flip_animation()

    def reposition(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def get_value(self):
        return CARD_VALUES[self.value]

    def flip_animation(self):
        data.animation_tracker.append(self)
        self.animation = FlipAnimation(self.front, self.back, self.face_up)
        
    def move_animation(self, end_position: tuple[float], duration: float):
        data.animation_tracker.append(self)
        self.animation = MoveAnimation(self.rect.topleft, end_position, duration)
