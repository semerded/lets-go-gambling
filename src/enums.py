from enum import Enum, StrEnum
from gFrame.colors import Color

class cardType(Enum):
    hearts = (Color.RED, '\u2665')
    spades = (Color.BLACK, '\u2660')
    diamonds = (Color.RED, '\u2666')
    clubs = (Color.BLACK, '\u2663')
    
class gameStatus(StrEnum):
    blackjack = "Blackjack" # you have 21
    bust = "Bust" # you have higher than 21
    push = "Push" # you have the same as the dealer
    win = "Win" # you have higher than the dealer
    lose = "Lose" # you have lower than the dealer
    hit = "Hit" # you get cards
    stand = "Stand" # you don't get any cards anymore, the dealer starts getting his cards
    init = "Dealing" # when the first cards are being dealt
    repack = "Repacking" # when the cards are being put back on the deck
    
    