import pygame as pg
import gFrame as gf
from src import data
from src.enums import pages, gameStatus
from src.frontend.components.center_text import CenterText
from src.frontend.components.textbox import TextBox
from src.backend.backend import daily_bonus_eta, can_use_daily_bonus


BACKGROUND = pg.image.load("assets/img/bg.jpg")
BACKGROUND = pg.transform.smoothscale(
    BACKGROUND, (gf.ScreenUnit.vw(100), gf.ScreenUnit.vh(100)))


press_to_start_text = CenterText("Press A to start", gf.Font.customFont(int(gf.ScreenUnit.vw(8)), "assets/font/CasinoShadow.ttf"), gf.Color.WHITE, (gf.ScreenUnit.vw(50), gf.ScreenUnit.vh(80)), fade_in_time=0.6, fade_out_time=0.2)
info_text = TextBox(gf.ScreenUnit.vw(5), gf.ScreenUnit.vh(5), gf.ScreenUnit.vw(60), gf.Font.FONT50, gf.Color.LESS_WHITE)

def page():
    
    if gf.Interactions.isKeyClicked(pg.K_SPACE) or data.phys_buttons.hit_button.is_clicked():
        data.active_page = pages.game
        data.game_state = gameStatus.init
    
    text = f'Welcome {data.current_player["name"]}\nYour current balance is: {data.current_player["balance"]}\n\n{daily_bonus_eta(data.current_player_id)}'
    info_text.set_text(text)    
        
    if data.APP.drawElements():
        data.APP_SURFACE.blit(BACKGROUND, (0, 0))
        info_text.draw(data.APP_SURFACE)
        press_to_start_text.draw()
        