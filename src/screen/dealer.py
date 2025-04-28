import gFrame as gf
from src.screen.player import Player
from src.screen.card_deck_handler import CardDeckHandler
from src.enums import gameStatus
from src.data import CARD_VALUES

class Dealer(Player):
    def __init__(self, card_deck_handler: CardDeckHandler):
        super().__init__(card_deck_handler)
        self.card_y = 0
        
    def get_score(self):
        score = 0
        ace_count = 0

        for card in self.hand:
            score += CARD_VALUES[card.value]
            if card == 'A':
                ace_count += 1

        # adjust for Aces if score is too high
        while score > 21 and ace_count > 0:
            score -= 10
            ace_count -= 1

        self.score = score