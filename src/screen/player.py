from src.screen.card_deck_handler import CardDeckHandler
from src.screen.components.card import Card
from src.enums import gameStatus
from src.data import CARD_VALUES
import gFrame as gf
from src import data

class Player:
    def __init__(self, card_deck_handler: CardDeckHandler):
        self.score: int = 0
        self.hand: list[Card] = []
        self.deck: CardDeckHandler = card_deck_handler
        self._stand = False
        self.card_y = gf.ScreenUnit.vh(100) - data.CARD_DIMENSIONS[1]
        
    def get_card(self, face_up: bool = True):
        card = self.deck.get_card(face_up)
        self.hand.append(card)
        if face_up:
            card.flip_animation()
        
    def stand(self) -> None:
        self._stand = True
        self.deck.game_status = gameStatus.stand
        
    def get_score(self):
        score = 0
        ace_count = 0

        for card in self.hand:
            score += CARD_VALUES[card.value]
            if card.value == 'A':
                ace_count += 1

        # adjust for Aces if score is too high
        while score > 21 and ace_count > 0:
            score -= 10
            ace_count -= 1

        self.score = score
        if self.score == 21:
            data.game_state = gameStatus.blackjack
        elif self.score > 21:
            data.game_state = gameStatus.bust
    
    def draw(self) -> None:
        for index, card in enumerate(self.hand):
            card.draw()
    