from src.enums import cardType
import gFrame as gf
from src.data import CARD_VALUES
from src import data
import pygame as pg
from src.frontend.animation.flip_animation import FlipAnimation
from src.frontend.components.rounded_surface_corners import round_corners
from src.frontend.animation.move_animation import MoveAnimation


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

        self.animations = []

    def _create_front_surface(self):
        self.front.convert_alpha()
        img = pg.image.load(
            f"assets/img/cards/{self.type.name[0].upper()}{self.value}.png").convert_alpha()
        img = pg.transform.smoothscale(img, data.CARD_DIMENSIONS)
        img = round_corners(img, int(gf.ScreenUnit.vw(1)))

        self.front.blit(img, (0, 0))

    def update(self):
        if len(self.animations) != 0:
            running_animations = []
            for animation in self.animations:
                if not animation.is_done() :
                    self.current_surface, self.rect = animation.animate(
                        self.current_surface, self.rect)
                    running_animations.append(animation)
            self.animations = running_animations
            if len(self.animations) == 0:
                data.animation_tracker.remove(self)

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
        self._add_animation()
        self.animations.append(FlipAnimation(self.front, self.back, self.face_up))

    def move_animation(self, end_position: tuple[float], duration: float):
        self._add_animation()
        self.animations.append(MoveAnimation(
            self.rect.topleft, end_position, duration))

    def _add_animation(self):
        if self not in data.animation_tracker:
            data.animation_tracker.append(self)
