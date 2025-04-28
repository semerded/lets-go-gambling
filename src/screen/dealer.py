import gFrame as gf
from src.screen.player import Player
from src.screen.card_deck_handler import CardDeckHandler
from src.enums import gameStatus

class Dealer(Player):
    def __init__(self, card_deck_handler: CardDeckHandler):
        super().__init__(card_deck_handler)
        self.card_y = 0