import gFrame as gf
from src import data
from src.enums import gameStatus

class ScoreTracker:
    light_count_x = 25
    light_count_y = 10
    def __init__(self):
        self.rect = gf.Rect(gf.ScreenUnit.vw(5), gf.ScreenUnit.vh(40), gf.ScreenUnit.vw(60), gf.ScreenUnit.vh(20))
        font = gf.Font.customFont(int(gf.ScreenUnit.vw(4)), "assets/font/CasinoShadow.ttf")
        
        self.player_text = gf.Text("Player: 0", font, gf.Color.WHITE)
        self.dealer_text = gf.Text("Dealer: 0", font, gf.Color.WHITE)
        
        self.game_state_rect = gf.Rect(gf.ScreenUnit.vw(35), gf.ScreenUnit.vh(40), gf.ScreenUnit.vw(30), gf.ScreenUnit.vh(20))
        font = gf.Font.customFont(int(gf.ScreenUnit.vw(8)), "assets/font/CasinoShadow.ttf")
        self.game_state_text = gf.Text("", font, gf.Color.WHITE)
        
        self.img = gf.Image("assets/img/game-state-textbox.jpg")
        self.img.resize(gf.ScreenUnit.vw(46), gf.ScreenUnit.vh(25))
    

        
    def update(self, player_score, dealer_score):
        self.player_text.setText(f"Player: {player_score}")
        self.dealer_text.setText(f"Dealer: {dealer_score}")
        
    
    def draw(self):
        self.img.place(gf.ScreenUnit.vw(27), gf.ScreenUnit.vh(37))
        self.dealer_text.placeInRect(self.rect, gf.xTextPositioning.left, gf.yTextPositioning.top)
        self.player_text.placeInRect(self.rect, gf.xTextPositioning.left, gf.yTextPositioning.bottom)
        if data.game_state in (gameStatus.init, gameStatus.repack):
            pass
        else:
            self.game_state_text.setText(data.game_state.name)
            if data.game_state in (gameStatus.blackjack, gameStatus.bust, gameStatus.win, gameStatus.lose, gameStatus.push):
                self.game_state_text.placeInRect(self.game_state_rect)
            elif len(data.animation_tracker) == 0:
                self.game_state_text.placeInRect(self.game_state_rect)
        