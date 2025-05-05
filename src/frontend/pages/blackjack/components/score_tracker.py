import gFrame as gf
from src import data
from src.frontend.pages.blackjack.player import Player

class ScoreTracker:
    light_count_x = 25
    light_count_y = 10

    def __init__(self, player: Player, player_second_hand: Player, dealer: Player):
        self.player = player
        self.dealer = dealer
        self.player_second_hand = player_second_hand
        self.rect = gf.Rect(gf.ScreenUnit.vw(5), gf.ScreenUnit.vh(
            40), gf.ScreenUnit.vw(90), gf.ScreenUnit.vh(20))
        font = gf.Font.customFont(
            int(gf.ScreenUnit.vw(4)), "assets/font/CasinoShadow.ttf")
        

        self.player_text = gf.Text("Player: 0", font, gf.Color.WHITE)
        self.dealer_text = gf.Text("Dealer: 0", font, gf.Color.WHITE)
        self.second_hand_text = gf.Text("Hand 2: 0", font, gf.Color.WHITE)

    def update(self):
        if data.splitted and self != None:
            if self.player.result == data.gameStatus.blackjack:
                self.player_text.setTextColor(gf.Color.GREEN)
            elif self.player.result == data.gameStatus.bust:
                self.player_text.setTextColor(gf.Color.RED)
            if self.player_second_hand.result == data.gameStatus.blackjack:
                self.second_hand_text.setTextColor(gf.Color.GREEN)
            elif self.player_second_hand.result == data.gameStatus.bust:
                self.second_hand_text.setTextColor(gf.Color.RED)
                
            self.player_text.setText(f"Hand 1: {self.player.score}")
            self.second_hand_text.setText(f"Hand 2: {self.player_second_hand.score}")
        else:
            self.player_text.setText(f"Player: {self.player.score}")
        self.dealer_text.setText(f"Dealer: {self.dealer.score}")

    def draw(self):
        self.dealer_text.placeInRect(
            self.rect, gf.xTextPositioning.left, gf.yTextPositioning.top)
        self.player_text.placeInRect(
            self.rect, gf.xTextPositioning.left, gf.yTextPositioning.bottom)
        
        if data.splitted:
            self.second_hand_text.placeInRect(
                self.rect, gf.xTextPositioning.right, gf.yTextPositioning.bottom)
            
    def reset(self):
        self.player_text.setText("Player: 0")
        self.player_text.setTextColor(gf.Color.WHITE)
        self.dealer_text.setText("Dealer: 0")
        self.dealer_text.setTextColor(gf.Color.WHITE)
        self.second_hand_text.setText("")
        self.second_hand_text.setTextColor(gf.Color.WHITE)
        
