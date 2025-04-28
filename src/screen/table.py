from src.screen.player import Player
from src.screen.dealer import Dealer
from src.screen.card_deck_handler import CardDeckHandler
from src import data

class Table:
    def __init__(self):
        self.deck = CardDeckHandler()
        self.player = Player(self.deck)
        self.dealer = Dealer(self.deck)
        self.stage = 0
        self.dealer_card_down = True
        
        
    def init_card_handler(self):
        match self.stage:
            case 0:
                self.player.get_card(face_up=False)
                self.stage += 1
            case 1:
                self.player.hand[-1].move_animation((0, self.player.card_y), 0.5)
                self.stage += 1
            case 2:
                self.player.hand[-1].flip()
                self.stage += 1
            case 3:
                self.player.get_score()
                self.dealer.get_card(face_up=False)
                self.stage += 1
            case 4:
                self.dealer.hand[-1].move_animation((0, self.dealer.card_y), 0.5)
                self.stage += 1
            case 5:
                self.dealer.hand[-1].flip()
                self.stage += 1
            case 6:
                self.dealer.get_score()
                self.player.get_card(face_up=False)
                self.stage += 1
            case 7:
                self.player.hand[-1].move_animation((data.CARD_DIMENSIONS[0] / 2, self.player.card_y), 0.5)
                self.stage += 1
            case 8:
                self.player.hand[-1].flip()
                self.stage += 1
            case 9:
                self.player.get_score()
                self.dealer.get_card(face_up=False)
                self.stage += 1   
            case 10:
                self.dealer.hand[-1].move_animation((data.CARD_DIMENSIONS[0] / 2, self.dealer.card_y), 0.5)
                data.game_state = data.gameStatus.hit   
    def hit_handler(self):
        match self.stage:
            case 0:
                self.player.get_card(face_up=False)
                self.stage += 1
            case 1:
                self.player.hand[-1].move_animation((data.CARD_DIMENSIONS[0] * ((len(self.player.hand) - 1) / 2), self.player.card_y), 0.5)
                self.stage += 1
            case 2:
                self.player.hand[-1].flip()
                self.stage += 1
            case 3:
                self.player.get_score()
                self.stage += 1
                
    def stand_handler(self):
        if self.dealer_card_down:
            match self.stage:
                case 0:
                    self.dealer.hand[-1].flip()
                    self.stage += 1
                case 1:
                    self.dealer.get_score()
                    self.stage = 0
                    self.dealer_card_down = False
        else:
            match self.stage:
                case 0:
                    self.dealer.get_card(face_up=False)
                    self.stage += 1
                case 1:
                    self.dealer.hand[-1].move_animation((data.CARD_DIMENSIONS[0] * ((len(self.dealer.hand) - 1) / 2), self.dealer.card_y), 0.5)
                    self.stage += 1
                case 2:
                    self.dealer.hand[-1].flip()
                    self.stage += 1
                case 3:
                    self.dealer.get_score()
                    if self.dealer.score < 17:
                        self.stage = 0
                    else:
                        self.stage += 1
                        self.compare_score()
                    
                    
                    
    def compare_score(self):
        if self.dealer.score > 21:
            data.game_state = data.gameStatus.win
        elif self.player.score == self.dealer.score:
            data.game_state = data.gameStatus.push
        elif self.player.score > self.dealer.score:
            data.game_state = data.gameStatus.win
        else:
            data.game_state = data.gameStatus.lose
        
    def draw(self):
        self.deck.draw()
        self.player.draw()
        self.dealer.draw()
        