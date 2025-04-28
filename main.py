import gFrame as gf
import pygame as pg
from src.enums import gameStatus
from src import data
from src.screen.card_deck_handler import CardDeckHandler, cardType
from src.screen.components.card import Card
from src.screen.table import Table
from gFrame import vars
from src.screen.components.rounded_surface_corners import round_corners

data.APP = gf.AppConstructor(data.APP_WIDTH, 800) # 200 doesn't matter and is overwritten on the line below
gf.Display.setAspectRatio(gf.aspectRatios.ratio16to9, data.APP_WIDTH)
data.APP_SURFACE = vars.mainDisplay
data.CARD_DIMENSIONS = (gf.ScreenUnit.vw(12), gf.ScreenUnit.vh(32))
data.CARD_BACK = pg.transform.scale(data.CARD_BACK, data.CARD_DIMENSIONS).convert_alpha()
data.CARD_BACK = round_corners(data.CARD_BACK, int(gf.ScreenUnit.vw(1)))
pg.draw.rect(data.CARD_BACK, gf.Color.LIGHT_GRAY, data.CARD_BACK.get_rect(), 1, int(gf.ScreenUnit.vw(1)))

table = Table()
table.deck.shuffle()    

if __name__ == "__main__":
    while data.running:
        data.APP.eventHandler(30)
        data.APP.fill(gf.Color.DARKMODE)
        if len(data.animation_tracker) == 0:
            match data.game_state:
                case gameStatus.init:
                    table.init_card_handler()
                case gameStatus.hit:
                    if gf.Interactions.isKeyClicked(pg.K_SPACE):
                        table.stage = 0
                    elif gf.Interactions.isKeyClicked(pg.K_RETURN):
                        data.game_state = gameStatus.stand
                        table.stage = 0
                    else:
                        table.hit_handler()
                case gameStatus.stand:
                    table.stand_handler()
            
            print(data.game_state, table.player.score, table.dealer.score)
        
            
        if data.APP.drawElements():
                table.draw()        

        