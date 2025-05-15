import pygame as pg
from typing import Callable
from gFrame.core.appConstructor import AppConstructor
from src.enums import gameStatus, pages, cardReaderState
from typing import TYPE_CHECKING

from src.backend.ble_button import BleButton_Handler

# Frontend

APP_WIDTH: str = "80dw"

running: bool = True
debugging: bool = True

CARD_VALUES: dict[str, int] = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
        '7': 7, '8': 8, '9': 9, '10': 10,
        'J': 10, 'Q': 10, 'K': 10, 'A': 11
    }

animation_tracker: list[Callable] = []

game_state = gameStatus.start
active_page = pages.idle

split_possible: bool = False
splitted: bool = False

APP: AppConstructor = None

CARD_DIMENSIONS = None

CARD_BACK: pg.Surface = pg.image.load("assets/img/card-back.png")

POKER_CHIPS: list[pg.Surface] = []
for i in range(1, 5):
    POKER_CHIPS.append(pg.image.load(f"assets/img/pokerchips/pokerchip{i}.png"))

APP_SURFACE: pg.Surface = None

# Card reader

card_reader_available: bool = False
card_inserted = False
card_data = None
card_reader_thread_running = False

card_reader_state: cardReaderState = cardReaderState.noCard


# Database

DATABASE_PATH: str = "src/database/players.json"
player_data: dict[str, dict] = {}

current_player_id: str = None
current_player: dict = {}

# io
io_available = True
phys_buttons: BleButton_Handler = BleButton_Handler(False)

