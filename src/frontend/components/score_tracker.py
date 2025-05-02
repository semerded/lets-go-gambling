import gFrame as gf
from src import data

class ScoreTracker:
    light_count_x = 25
    light_count_y = 10

    def __init__(self):
        self.rect = gf.Rect(gf.ScreenUnit.vw(5), gf.ScreenUnit.vh(
            40), gf.ScreenUnit.vw(90), gf.ScreenUnit.vh(20))
        font = gf.Font.customFont(
            int(gf.ScreenUnit.vw(4)), "assets/font/CasinoShadow.ttf")
        

        self.player_text = gf.Text("Player: 0", font, gf.Color.WHITE)
        self.dealer_text = gf.Text("Dealer: 0", font, gf.Color.WHITE)
        self.second_hand_text = gf.Text("Hand 2: 0", font, gf.Color.WHITE)

    def update(self, player_score, dealer_score, second_hand_score = None):
        if data.splitted and second_hand_score != None:
            self.player_text.setText(f"Hand 1: {player_score}")
            self.second_hand_text.setText(f"Hand 2: {second_hand_score}")
        else:
            self.player_text.setText(f"Player: {player_score}")
        self.dealer_text.setText(f"Dealer: {dealer_score}")

    def draw(self):
        self.dealer_text.placeInRect(
            self.rect, gf.xTextPositioning.left, gf.yTextPositioning.top)
        self.player_text.placeInRect(
            self.rect, gf.xTextPositioning.left, gf.yTextPositioning.bottom)
        
        if data.splitted:
            self.second_hand_text.placeInRect(
                self.rect, gf.xTextPositioning.right, gf.yTextPositioning.bottom)
