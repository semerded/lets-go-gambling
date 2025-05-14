from enum import Enum
from gFrame.colors import Color

class cardType(Enum):
    hearts = (Color.RED, '\u2665')
    spades = (Color.BLACK, '\u2660')
    diamonds = (Color.RED, '\u2666')
    clubs = (Color.BLACK, '\u2663')
    
class gameStatus(Enum):
    blackjack = ("Blackjack!", Color.GREEN) # you have 21
    bust = ("Bust", Color.RED) # you have higher than 21
    push = ("Push", Color.WHITE) # you have the same as the dealer
    win = ("You win!", Color.GREEN) # you have higher than the dealer
    lose = ("You lose!", Color.RED) # you have lower than the dealer
    hit = ("Hit!", Color.WHITE) # you get cards
    stand = ("Standing", Color.WHITE) # you don't get any cards anymore, the dealer starts getting his cards
    init = ("Dealing,,,", Color.WHITE) # when the first cards are being dealt
    repack = ("Shuffling,,,", Color.WHITE) # when the cards are being put back on the deck
    splitting = ("Splitting", Color.WHITE)
    splitResult = ("Split Result", Color.WHITE)
    bigWin = ("BIG WIN", Color.WHITE)
    start = ("Btn A to Start", Color.WHITE)
    
class pages(Enum):
    idle = 0
    login = 1
    register = 2
    start = 3
    game = 4
    
class cardReaderState(Enum):
    noCard = "No card inserted"
    cardInserted = "Card inserted"
    badRead = "Failed to read card"
    succes = "Card read successfully"
    
    