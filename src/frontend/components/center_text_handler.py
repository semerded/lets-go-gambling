from src.frontend.components.center_text import CenterText
import gFrame as gf
from src import data
from src.enums import gameStatus

class CenterTextHandler:
    def __init__(self):
        self.center_text: CenterText = None
        self.center_text_buffer: CenterText = None
        
        self.previous_game_state = None
        self.center_text_font = gf.Font.customFont(int(gf.ScreenUnit.vw(8)), "assets/font/CasinoShadow.ttf")

    def set_center_text(self, text: str, color):
        if self.center_text is not None:
            self.center_text.stop()
            self.center_text_buffer = self.center_text
        self.center_text = CenterText(text, self.center_text_font, color, (gf.ScreenUnit.vw(50), gf.ScreenUnit.vh(50)), fade_in_time=0.6, fade_out_time=0.2)
        
        
    def update(self):
        if data.game_state != self.previous_game_state:
            self.previous_game_state = data.game_state
            self.set_center_text(*data.game_state.value)
            # if data.game_state == gameStatus.blackjack:
            #     self.set_center_text(data.game, gf.Color.WHITE)
            # elif data.game_state == gameStatus.bust:
            #     self.set_center_text("BUST", gf.Color.REDWOOD)
            # elif data.game_state == gameStatus.win:
            #     self.set_center_text("WIN", gf.Color.GREEN)
            # elif data.game_state == gameStatus.lose:
            #     self.set_center_text("LOSE", gf.Color.REDWOOD)
            # elif data.game_state == gameStatus.push:
            #     self.set_center_text("PUSH", gf.Color.WHITE)
            # elif data.game_state == gameStatus.hit:
            #     self.set_center_text("HIT", gf.Color.WHITE)
            # elif data.game_state == gameStatus.stand:
            #     self.set_center_text("STAND", gf.Color.WHITE)
        
    def draw(self):    
        self.update()    
        if self.center_text is not None:
            if self.center_text.is_done():
                self.center_text = None
            else:
                self.center_text.draw()
        if self.center_text_buffer is not None:
            if self.center_text_buffer.is_done():
                self.center_text_buffer = None
            else:
                self.center_text_buffer.draw()
                
                
                