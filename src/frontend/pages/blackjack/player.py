from src.frontend.pages.blackjack.card_deck_handler import CardDeckHandler
from src.frontend.pages.blackjack.components.card import Card
from src.enums import gameStatus
from src.data import CARD_VALUES
import gFrame as gf
from src import data
from src.frontend.pages.blackjack.components.moving_fading_text import MovingFadingText

class Player:
    def __init__(self, card_deck_handler: CardDeckHandler, positioned_left: bool = True):
        self.score: int = 0
        self.hand: list[Card] = []
        self.deck: CardDeckHandler = card_deck_handler
        self.standing = False
        self.positioned_left = positioned_left
        if positioned_left:
            self.card_x = gf.ScreenUnit.vw(5)
        else:
            self.card_x = gf.ScreenUnit.vw(95) - data.CARD_DIMENSIONS[0]
        self.card_y = gf.ScreenUnit.vh(95) - data.CARD_DIMENSIONS[1]
        self.animated_text = None
        self.result = None
        self.double_down = False

        
    def get_card(self, face_up: bool = True):
        card = self.deck.get_card(face_up)
        self.hand.append(card)
        if face_up:
            card.flip_animation()
        self.card_get_animation()
            
            
    def card_get_animation(self):
        direction = 1 if self.positioned_left else -1
        x_deviation = data.CARD_DIMENSIONS[0] * ((len(self.hand) - 1) / 2) * direction
        self.hand[-1].move_animation((self.card_x + x_deviation, self.card_y), 0.5, 90)
            
    def show_animated_text(self, text: str, color):
        x = self.hand[-1].rect.x
        y = self.card_y + data.CARD_DIMENSIONS[1] / 2
        if self.positioned_left:
            x_end = x + data.CARD_DIMENSIONS[0] * 3
        else:
            x_end = x - data.CARD_DIMENSIONS[0] * 3
        
        self.animated_text = MovingFadingText(text, color, 2, (x, y), (x_end, y))
        
    def get_score(self):
        if self.result is None:
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
            
    def activate_animation(self):
        for card in self.hand:
            card.activate_animation()
            
    def deactivate_animation(self):
        for card in self.hand:
            card.deactivate_animation()
    
    def draw(self) -> None:
        if self.animated_text is not None:
            self.animated_text.draw()
        for index, card in enumerate(self.hand):
            card.draw()
    