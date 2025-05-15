from src import data
import gFrame as gf
import pygame as pg
from src.frontend.pages.blackjack.table import Table
from src.frontend.pages.blackjack.components.rounded_surface_corners import round_corners
from src.enums import gameStatus, pages
from src.frontend.components.dialog import Dialog

data.CARD_DIMENSIONS = (gf.ScreenUnit.vw(12), gf.ScreenUnit.vh(32))
data.CARD_BACK = pg.transform.smoothscale(
    data.CARD_BACK, data.CARD_DIMENSIONS).convert_alpha()
data.CARD_BACK = round_corners(data.CARD_BACK, int(gf.ScreenUnit.vw(1)))
pg.draw.rect(data.CARD_BACK, gf.Color.LIGHT_GRAY,
             data.CARD_BACK.get_rect(), 1, int(gf.ScreenUnit.vw(1)))

BACKGROUND = pg.image.load("assets/img/bg.jpg")
BACKGROUND = pg.transform.smoothscale(
    BACKGROUND, (gf.ScreenUnit.vw(100), gf.ScreenUnit.vh(100)))

table = Table()
table.deck.shuffle()

def bail_out_accept():
    global show_bail_out_dialog
    data.game_state = gameStatus.start
    data.active_page = pages.start
    show_bail_out_dialog = False
    
def bail_out_decline():
    global show_bail_out_dialog
    show_bail_out_dialog = False
    
bail_out_dialog = Dialog(
    "Are you sure you want to bail out of the game? Active bets will be lost", on_accept=bail_out_accept, on_cancel=bail_out_decline)
show_bail_out_dialog = False

def page():
    global show_bail_out_dialog

    if data.game_state == gameStatus.start and data.phys_buttons.b_button.is_clicked() or gf.Interactions.isKeyClicked(pg.K_b):
        data.active_page = pages.start
    elif data.phys_buttons.b_button.is_held_for(0.5) or gf.Interactions.isKeyClicked(pg.K_b):
        show_bail_out_dialog = True
        print("bail out")
    
    if show_bail_out_dialog:
        bail_out_dialog.draw(data.APP_SURFACE)
    
    else:
        data.APP_SURFACE.blit(BACKGROUND, (0, 0))
        if len(data.animation_tracker) == 0:           
            match data.game_state:
                case gameStatus.init:
                        
                    table.init_card_handler()
                
                case gameStatus.hit:
                    # if data.split_possible and (gf.Interactions.isKeyClicked(pg.K_s) or data.phys_buttons.y_button.is_clicked():
                    #     table.split_hand()
                    #     data.split_possible = False
                    
                    if gf.Interactions.isKeyClicked(pg.K_s) or data.phys_buttons.y_button.is_clicked(): #? only for testing
                        table.split_hand()
                        data.split_possible = False
                    
                    elif gf.Interactions.isKeyClicked(pg.K_SPACE) or data.phys_buttons.hit_button.is_clicked():
                        table.stage = 0
                        
                    elif gf.Interactions.isKeyClicked(pg.K_RETURN) or data.phys_buttons.stand_button.is_clicked():
                        table.stand()
                        
                        if not data.splitted or (table.player.standing and table.player_second_hand.standing) or (table.player.result is not None and table.player_second_hand.standing) or (table.player.standing and table.player_second_hand.result is not None):
                            table.stage = 0
                    else:
                        table.hit_handler()
                        
                case gameStatus.splitting:
                    table.split_handler()
                case gameStatus.stand:
                    table.stand_handler()
                case gameStatus.repack:
                    table.repack_handler()
                    
                case gameStatus.start:
                    if gf.Interactions.isKeyClicked(pg.K_SPACE) or data.phys_buttons.a_button.is_clicked():
                        data.game_state = gameStatus.init
            
            # print(data.game_state)

            if data.game_state in (gameStatus.blackjack, gameStatus.bust, gameStatus.win, gameStatus.lose, gameStatus.push, gameStatus.bigWin, gameStatus.splitResult):
                if gf.Interactions.isKeyClicked(pg.K_RETURN) or data.phys_buttons.any_clicked():
                    table.stage = 0
                    data.game_state = gameStatus.repack
            elif data.game_state != gameStatus.repack:
                table.table_handler()

        if data.APP.drawElements():
            table.draw()
