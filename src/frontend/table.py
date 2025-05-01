from src.frontend.player import Player
from src.frontend.dealer import Dealer
from src.frontend.card_deck_handler import CardDeckHandler
from src.frontend.components.score_tracker import ScoreTracker
from src import data
import gFrame as gf
from src.frontend.components.center_text_handler import CenterTextHandler

class Table:
    def __init__(self):
        self.deck = CardDeckHandler()
        self.player = Player(self.deck)
        self.dealer = Dealer(self.deck)
        self.score_tracker = ScoreTracker()
        self.stage = 0
        self.dealer_card_down = True
        self.center_text_handler = CenterTextHandler()
        
    def init_card_handler(self):
        match self.stage:
            case 0:
                self.player.get_card(face_up=False)
                self.stage += 1
            case 1:
                self.player.hand[-1].move_animation((gf.ScreenUnit.vw(5), self.player.card_y), 0.5)
                self.stage += 1
            case 2:
                self.player.hand[-1].flip()
                self.stage += 1
            case 3:
                self.player.get_score()
                self.score_tracker.update(self.player.score, self.dealer.score)
                self.dealer.get_card(face_up=False)
                self.stage += 1
            case 4:
                self.dealer.hand[-1].move_animation((gf.ScreenUnit.vw(5), self.dealer.card_y), 0.5)
                self.stage += 1
            case 5:
                self.dealer.hand[-1].flip()
                self.stage += 1
            case 6:
                self.dealer.get_score()
                self.score_tracker.update(self.player.score, self.dealer.score)
                self.player.get_card(face_up=False)
                self.stage += 1
            case 7:
                self.player.hand[-1].move_animation((gf.ScreenUnit.vw(5) + data.CARD_DIMENSIONS[0] / 2, self.player.card_y), 0.5)
                self.stage += 1
            case 8:
                self.player.hand[-1].flip()
                self.stage += 1
            case 9:
                self.player.get_score()
                self.score_tracker.update(self.player.score, self.dealer.score)
                self.dealer.get_card(face_up=False)
                self.stage += 1   
            case 10:
                self.dealer.hand[-1].move_animation((gf.ScreenUnit.vw(5) + data.CARD_DIMENSIONS[0] / 2, self.dealer.card_y), 0.5)
                data.game_state = data.gameStatus.hit   
                
    def hit_handler(self):
        match self.stage:
            case 0:
                self.player.get_card(face_up=False)
                self.stage += 1
            case 1:
                self.player.hand[-1].move_animation((gf.ScreenUnit.vw(5) + data.CARD_DIMENSIONS[0] * ((len(self.player.hand) - 1) / 2), self.player.card_y), 0.5)
                self.stage += 1
            case 2:
                self.player.hand[-1].flip()
                self.stage += 1
            case 3:
                self.player.get_score()
                self.score_tracker.update(self.player.score, self.dealer.score)
                self.stage += 1
                
    def stand_handler(self):
        if self.dealer_card_down:
            match self.stage:
                case 0:
                    self.dealer.hand[-1].flip()
                    self.stage += 1
                case 1:
                    self.dealer.get_score()
                    self.score_tracker.update(self.player.score, self.dealer.score)
                    if self.dealer.score < 17:
                        self.stage = 0
                        self.dealer_card_down = False
                    else:
                        self.stage += 1
                        self.compare_score()
        else:
            match self.stage:
                case 0:
                    self.dealer.get_card(face_up=False)
                    self.stage += 1
                case 1:
                    self.dealer.hand[-1].move_animation((gf.ScreenUnit.vw(5) + data.CARD_DIMENSIONS[0] * ((len(self.dealer.hand) - 1) / 2), self.dealer.card_y), 0.5)
                    self.stage += 1
                case 2:
                    self.dealer.hand[-1].flip()
                    self.stage += 1
                case 3:
                    self.dealer.get_score()
                    self.score_tracker.update(self.player.score, self.dealer.score)
                    if self.dealer.score < 17:
                        self.stage = 0
                    else:
                        self.stage += 1
                        self.compare_score()
    
    def repack_handler(self):
        match self.stage:
            case 0:
                for card in self.player.hand:
                    card.flip()
                for card in self.dealer.hand:
                    if card.face_up:
                        card.flip()
                self.stage += 1
            case 1:
                x_pos = self.deck.card_deck[-1].rect.x
                y_pos = self.deck.card_deck[-1].rect.y
                for card in self.player.hand:
                    card.move_animation((x_pos, y_pos), 0.5)
                for card in self.dealer.hand:
                    card.move_animation((x_pos, y_pos), 0.5)
                self.stage += 1
            case 2:
                self.deck.card_deck.extend(self.player.hand + self.dealer.hand)
                self.stage += 1
            case 3:
                self.reset()
                self.deck.shuffle()
                self.deck.reorder_deck()
                data.game_state = data.gameStatus.init
                self.stage = 0
                    
                    
    def compare_score(self):
        if self.dealer.score > 21:
            data.game_state = data.gameStatus.win
            self.dealer.show_animated_text("BUST", gf.Color.REDWOOD)
        elif self.dealer.score == 21 and self.player.score < 21:
            self.dealer.show_animated_text("BLACKJACK", gf.Color.WHITE)
            data.game_state = data.gameStatus.lose
        elif self.player.score == self.dealer.score:
            data.game_state = data.gameStatus.push
        elif self.player.score > self.dealer.score:
            data.game_state = data.gameStatus.win
        else:
            data.game_state = data.gameStatus.lose
        
    def draw(self):
        self.score_tracker.draw()
        self.center_text_handler.draw()
        self.deck.draw()
        self.player.draw()
        self.dealer.draw()
        
    def reset(self):
        self.player.score = 0
        self.player.hand = []
        self.dealer.score = 0
        self.dealer.hand = []
        self.stage = 0
        self.dealer_card_down = True
        