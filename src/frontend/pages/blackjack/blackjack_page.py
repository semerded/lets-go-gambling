from src import data
import gFrame as gf
import pygame as pg
from src.frontend.pages.blackjack.table import Table
from src.frontend.pages.blackjack.components.rounded_surface_corners import round_corners
from src.enums import gameStatus

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

def page():
    data.APP_SURFACE.blit(BACKGROUND, (0, 0))
    if len(data.animation_tracker) == 0:           
        match data.game_state:
            case gameStatus.init:
                    
                table.init_card_handler()
            
            case gameStatus.hit:
                # if data.split_possible and gf.Interactions.isKeyClicked(pg.K_s):
                #     table.split_hand()
                #     data.split_possible = False
                
                if gf.Interactions.isKeyClicked(pg.K_s): #? only for testing
                    table.split_hand()
                    data.split_possible = False
                
                elif gf.Interactions.isKeyClicked(pg.K_SPACE):
                    table.stage = 0
                    
                elif gf.Interactions.isKeyClicked(pg.K_RETURN):
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
                if gf.Interactions.isKeyClicked(pg.K_SPACE):
                    data.game_state = gameStatus.init
        
        # print(data.game_state)

        if data.game_state in (gameStatus.blackjack, gameStatus.bust, gameStatus.win, gameStatus.lose, gameStatus.push, gameStatus.bigWin, gameStatus.splitResult):
            if gf.Interactions.isKeyClicked(pg.K_RETURN):
                table.stage = 0
                data.game_state = gameStatus.repack
        elif data.game_state != gameStatus.repack:
            table.table_handler()

    if data.APP.drawElements():
        table.draw()
