from src.frontend.components.card import Card
from src.enums import cardType
from random import shuffle
from src.data import CARD_VALUES
import gFrame as gf
from src import data

class CardDeckHandler:
    def __init__(self):
        self.card_deck: list[Card] = CardDeckHandler.generate_card_deck()
        self.hand_counter = 0
        
        
    @staticmethod
    def generate_card_deck():
        card_deck = []
        for card_type in cardType:
            for value in CARD_VALUES.keys():
                card_deck.append(Card(card_type, value))
        return card_deck

    def shuffle(self):
        shuffle(self.card_deck)
        self.reorder_deck()
        
    def reorder_deck(self):
        card_x_deviation = 0
        card_deck_start_x = gf.ScreenUnit.vw(100) - data.CARD_DIMENSIONS[0]
        card_deck_y = int(gf.ScreenUnit.vh(50) - (data.CARD_DIMENSIONS[1] / 2))
        for card in self.card_deck:
            card.rect.x = card_deck_start_x - card_x_deviation
            card.rect.y = card_deck_y 
            card_x_deviation += 3
        
        
    def get_card(self, face_up: bool = True):
        card = self.card_deck.pop()
        card.face_up = face_up
        return card
    
    def draw(self):
        for card in self.card_deck:
            card.draw()
    
    
    
    
        