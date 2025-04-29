import pygame as pg
from typing import Callable
from gFrame.core.appConstructor import AppConstructor
from src.enums import gameStatus

APP_WIDTH: str = "100dw"

running: bool = True
debugging: bool = True

CARD_VALUES: dict[str, int] = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
        '7': 7, '8': 8, '9': 9, '10': 10,
        'J': 10, 'Q': 10, 'K': 10, 'A': 11
    }

animation_tracker: list[Callable] = []

game_state = gameStatus.init

APP: AppConstructor = None

CARD_DIMENSIONS = None

CARD_BACK: pg.Surface = pg.image.load("assets/img/card-back.png")

APP_SURFACE: pg.Surface = None

