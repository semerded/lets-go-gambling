from src import data
import gFrame as gf
import pygame as pg
from src.frontend.pages.blackjack.table import Table
from src.frontend.pages.blackjack.components.rounded_surface_corners import round_corners
from src.enums import gameStatus, pages, LcdStatus
from src.frontend.components.dialog import Dialog
from src.frontend.components.button_guide import ButtonGuide

data.CARD_DIMENSIONS = (gf.ScreenUnit.vw(12), gf.ScreenUnit.vh(32))
data.CARD_BACK = pg.transform.smoothscale(
    data.CARD_BACK, data.CARD_DIMENSIONS).convert_alpha()
data.CARD_BACK = round_corners(data.CARD_BACK, int(gf.ScreenUnit.vw(1)))
pg.draw.rect(data.CARD_BACK, gf.Color.LIGHT_GRAY,
             data.CARD_BACK.get_rect(), 1, int(gf.ScreenUnit.vw(1)))

BACKGROUND = pg.image.load("assets/img/bg.jpg")
BACKGROUND = pg.transform.smoothscale(
    BACKGROUND, (gf.ScreenUnit.vw(100), gf.ScreenUnit.vh(100)))


start_game_button_guide = ButtonGuide("Start", "Start", "Raise bet", "Home", "Lower bet", "All in" )
hit_button_guide = ButtonGuide("Hit", "Stand", None , "Bail out", "Split", "Double down")
stand_button_guide = ButtonGuide(None, None, None, "Bail out", None)
end_game_button_guide = ButtonGuide(None, None, "Play again" , "Home")

table = Table()
table.deck.shuffle()

def bail_out_accept():
    global show_bail_out_dialog
    data.game_state = gameStatus.start
    data.active_page = pages.start
    show_bail_out_dialog = False
    data.ack_message_handler.set_state(LcdStatus.idle)
    data.current_player["balance"] -= data.current_bet
    data.mqqt_messenger.update_games_lost()
    data.mqqt_messenger.update_money_lost(data.current_bet)
    
def bail_out_decline():
    global show_bail_out_dialog
    show_bail_out_dialog = False
    
bail_out_dialog = Dialog(
    "Are you sure you want to bail out of the game? Active bets will be lost", on_accept=bail_out_accept, on_cancel=bail_out_decline)
show_bail_out_dialog = False


def page():
    global show_bail_out_dialog

    if data.game_state in (gameStatus.blackjack, gameStatus.bust, gameStatus.win, gameStatus.lose, gameStatus.push, gameStatus.bigWin, gameStatus.splitResult, gameStatus.start) and (data.phys_buttons.b_button.is_clicked() or gf.Interactions.isKeyClicked(pg.K_b)):
        data.active_page = pages.start
        data.current_bet = 10
        data.ack_message_handler.set_state(LcdStatus.idle)
        
    elif data.phys_buttons.b_button.is_held_for(0.5) or gf.Interactions.isKeyClicked(pg.K_c):
        show_bail_out_dialog = True
    if show_bail_out_dialog:
        bail_out_dialog.draw()
        return
    
    data.APP_SURFACE.blit(BACKGROUND, (0, 0))
    if len(data.animation_tracker) == 0:           
        match data.game_state:
            case gameStatus.init:
                data.ack_message_handler.set_pwm(0, 0)
                table.init_card_handler()
            
            case gameStatus.hit:
                # if data.split_possible and (gf.Interactions.isKeyClicked(pg.K_s) or data.phys_buttons.y_button.is_clicked():
                #     table.split_hand()
                #     data.split_possible = False
                data.ack_message_handler.set_pwm(99, 50)
                
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
                data.ack_message_handler.set_pwm(0, 50)
                
                table.split_handler()
            case gameStatus.stand:
                data.ack_message_handler.set_pwm(0, 0)
                table.stand_handler()
            case gameStatus.repack:
                data.ack_message_handler.set_pwm(0, 0)
                table.repack_handler()
                
            case gameStatus.start:
                data.ack_message_handler.set_pwm(99, 99)
                table.payed_out = False
                if gf.Interactions.isKeyClicked(pg.K_SPACE) or data.phys_buttons.hit_button.is_clicked() or data.phys_buttons.stand_button.is_clicked():
                    data.game_state = gameStatus.init
                    data.mqqt_messenger.update_games_played()
                    
                elif gf.Interactions.isKeyClicked(pg.K_a) or data.phys_buttons.a_button.is_clicked():
                    expected_bet = data.current_bet + 50
                    if expected_bet < 1000:
                        if expected_bet > data.current_player["balance"]:
                            data.current_bet = data.current_player["balance"]
                        else:
                            data.current_bet = expected_bet
                        
                elif gf.Interactions.isKeyClicked(pg.K_x) or data.phys_buttons.x_button.is_clicked():
                    expected_bet = data.current_bet - 50
                    if expected_bet > 0:
                        data.current_bet = expected_bet
                    else:
                        data.current_bet = 10
                elif gf.Interactions.isKeyClicked(pg.K_y) or data.phys_buttons.y_button.is_clicked():
                    if data.current_player["balance"] < 1000:
                        data.current_bet = data.current_player["balance"]
                    else:
                        data.current_bet = 1000
        
        # print(data.game_state)

        if data.game_state in (gameStatus.blackjack, gameStatus.bust, gameStatus.win, gameStatus.lose, gameStatus.push, gameStatus.bigWin, gameStatus.splitResult):
            data.ack_message_handler.set_pwm(0, 0)
            table.payout()
            if gf.Interactions.isKeyClicked(pg.K_RETURN) or data.phys_buttons.a_button.is_clicked():
                table.stage = 0
                data.game_state = gameStatus.repack
        elif data.game_state != gameStatus.repack:
            table.table_handler()

    if data.APP.drawElements():
        table.draw()
        match data.game_state:
            case gameStatus.start:
                start_game_button_guide.draw()
                data.ack_message_handler.set_state(LcdStatus.setBet)
            case gameStatus.hit:
                hit_button_guide.draw()
                data.ack_message_handler.set_state(LcdStatus.activeBet)
            case gameStatus.stand:
                stand_button_guide.draw()
                data.ack_message_handler.set_state(LcdStatus.activeBet)
            case gameStatus.repack:
                pass
            case gameStatus.splitting:
                pass
            case gameStatus.init:
                pass
            case _:
                data.ack_message_handler.set_state(LcdStatus.result)
                end_game_button_guide.draw()
