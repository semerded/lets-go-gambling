import pygame as pg
import gFrame as gf
from src import data
from random import randint
from src.frontend.pages.idle.falling_chip import FallingChip
from src.frontend.components.center_text import CenterText
from src.frontend.components.center_x import center_x
from src.enums import pages

for index, pokerchip in enumerate(data.POKER_CHIPS):
    data.POKER_CHIPS[index] = pg.transform.smoothscale(pokerchip, (gf.ScreenUnit.vw(3), gf.ScreenUnit.vw(3))).convert_alpha()
    
BACKGROUND = pg.image.load("assets/img/idle.jpg")
BACKGROUND = pg.transform.smoothscale(
    BACKGROUND, (gf.ScreenUnit.vw(100), gf.ScreenUnit.vh(100)))

poker_chip_list = []

title = CenterText("Smart Jack", gf.Font.customFont(int(gf.ScreenUnit.vw(12)), "assets/font/CasinoShadow.ttf"), gf.Color.WHITE, (gf.ScreenUnit.vw(50), gf.ScreenUnit.vh(50)), fade_in_time=0.6, fade_out_time=0.2)
subtitle = CenterText("The IOT Blackjack Game", gf.Font.customFont(int(gf.ScreenUnit.vw(4)), "assets/font/CasinoShadow.ttf"), gf.Color.WHITE, (gf.ScreenUnit.vw(50), gf.ScreenUnit.vh(65)), fade_in_time=0.6, fade_out_time=0.2)

start_text = gf.Text("Press Hit or Stand to start!", gf.Font.customFont(int(gf.ScreenUnit.vw(5)), "assets/font/CasinoShadow.ttf"), gf.Color.LESS_WHITE)
start_text_center_x = center_x(start_text)


def page():
    data.APP_SURFACE.blit(BACKGROUND, (0, 0))
    
    if len(poker_chip_list) < 15 and randint(0, 5) == 0:
        poker_chip_list.append(FallingChip())
    
    for poker_chip in poker_chip_list:
        poker_chip: FallingChip
        poker_chip.move()
        poker_chip.place()
        if poker_chip.is_descended_completely_into_the_abyss():
            poker_chip_list.remove(poker_chip)
    
    start_text.place(start_text_center_x, gf.ScreenUnit.vh(90))
    subtitle.draw()
    title.draw()    

    if gf.Interactions.isMouseClicked(pg.BUTTON_LEFT) or gf.Interactions.isKeyClicked(pg.K_SPACE) or data.phys_buttons.hit_button.is_clicked() or data.phys_buttons.stand_button.is_clicked():
        title.stop()
        subtitle.stop()
        
    if title.is_done() and subtitle.is_done():
        data.active_page = pages.login
    