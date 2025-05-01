import gFrame as gf
from src import data
from src.enums import gameStatus


class ScoreTracker:
    light_count_x = 25
    light_count_y = 10

    def __init__(self):
        self.rect = gf.Rect(gf.ScreenUnit.vw(5), gf.ScreenUnit.vh(
            40), gf.ScreenUnit.vw(60), gf.ScreenUnit.vh(20))
        font = gf.Font.customFont(
            int(gf.ScreenUnit.vw(4)), "assets/font/CasinoShadow.ttf")

        self.player_text = gf.Text("Player: 0", font, gf.Color.WHITE)
        self.dealer_text = gf.Text("Dealer: 0", font, gf.Color.WHITE)

    def update(self, player_score, dealer_score):
        self.player_text.setText(f"Player: {player_score}")
        self.dealer_text.setText(f"Dealer: {dealer_score}")

    def draw(self):
        self.dealer_text.placeInRect(
            self.rect, gf.xTextPositioning.left, gf.yTextPositioning.top)
        self.player_text.placeInRect(
            self.rect, gf.xTextPositioning.left, gf.yTextPositioning.bottom)
