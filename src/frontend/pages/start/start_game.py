import pygame as pg
import gFrame as gf
from src import data
from src.enums import pages, gameStatus
from src.frontend.components.center_text import CenterText
from src.frontend.components.textbox import TextBox
from src.backend.backend import daily_bonus_eta, can_use_daily_bonus, logout, claim_daily_bonus, save_current_player
from src.frontend.components.button_guide import ButtonGuide
from src.enums import LcdStatus
from src.frontend.components.dialog import Dialog


BACKGROUND = pg.image.load("assets/img/bg.jpg")
BACKGROUND = pg.transform.smoothscale(
    BACKGROUND, (gf.ScreenUnit.vw(100), gf.ScreenUnit.vh(100)))

button_guide = ButtonGuide(None, None, "Start", "Logout")
button_guide_can_claim_daily_bonus = ButtonGuide(None, None, "Start", "Logout", None, "Claim daily bonus")
press_to_start_text = CenterText("Lets Go Gambling!", gf.Font.customFont(int(gf.ScreenUnit.vw(8)), "assets/font/CasinoShadow.ttf"), gf.Color.WHITE, (gf.ScreenUnit.vw(50), gf.ScreenUnit.vh(80)), fade_in_time=0.6, fade_out_time=0.2)
info_text = TextBox(gf.ScreenUnit.vw(5), gf.ScreenUnit.vh(5), gf.ScreenUnit.vw(60), gf.Font.FONT50, gf.Color.LESS_WHITE)


def page():
    data.ack_message_handler.set_state(LcdStatus.idle)
    
    _can_use_daily_bonus = can_use_daily_bonus(data.current_player_id)
    
    if gf.Interactions.isKeyClicked(pg.K_b) or data.phys_buttons.b_button.is_clicked():
        logout()
        data.active_page = pages.idle
        return
        
    elif gf.Interactions.isKeyClicked(pg.K_SPACE) or data.phys_buttons.a_button.is_clicked():
        data.active_page = pages.game
        data.game_state = gameStatus.start
        
    elif (gf.Interactions.isKeyClicked(pg.K_y) or data.phys_buttons.y_button.is_clicked()) and _can_use_daily_bonus:
        claim_daily_bonus(data.current_player_id)
    
    if data.phys_buttons.hit_button.is_pressed() and data.phys_buttons.stand_button.is_pressed():
        if data.phys_buttons.y_button.is_clicked():
            print("Cheat activated")
            data.current_player["balance"] += 1000
            save_current_player()
    
    text = f'Welcome {data.current_player["name"]}\nYour current balance is: {data.current_player["balance"]}\n\n{daily_bonus_eta(data.current_player_id)}'
    info_text.set_text(text)    
    
        
        
    if data.APP.drawElements():
        data.APP_SURFACE.blit(BACKGROUND, (0, 0))
        info_text.draw(data.APP_SURFACE)
        press_to_start_text.draw()
        button_guide.draw()
        if _can_use_daily_bonus:
            button_guide_can_claim_daily_bonus.draw()
        else:
            button_guide.draw()
        