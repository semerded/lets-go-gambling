import pygame as pg
import gFrame as gf
from src import data
from src.frontend.animation.move_animation import MoveAnimation
from src.enums import cardReaderState, pages
from src.backend import backend

BG = pg.image.load("assets/img/eID/bg.jpg")
BG = pg.transform.smoothscale(BG, (gf.ScreenUnit.vw(100), gf.ScreenUnit.vh(100)))
BG.set_alpha(130)

SPECIMEN_BACK = pg.image.load("assets/img/eID/specimen-back.png")
SPECIMEN_BACK = pg.transform.rotate(SPECIMEN_BACK, 90)
SPECIMEN_BACK = pg.transform.smoothscale(SPECIMEN_BACK, (gf.ScreenUnit.vw(20), gf.ScreenUnit.vh(50)))
specimen_back_rect = SPECIMEN_BACK.get_rect()

card_move_up_animation = MoveAnimation(gf.ScreenUnit.vh(30), gf.ScreenUnit.vh(5), 1)
card_move_down_animation = MoveAnimation(gf.ScreenUnit.vh(5), gf.ScreenUnit.vh(30), 1)
card_moving_up = False
READER_BOTTOM = pg.image.load("assets/img/eID/reader-bottom.png")
READER_BOTTOM = pg.transform.smoothscale(READER_BOTTOM, (gf.ScreenUnit.vw(24), gf.ScreenUnit.vw(24)))
READER_TOP = pg.image.load("assets/img/eID/reader-top.png")
READER_TOP = pg.transform.smoothscale(READER_TOP, (gf.ScreenUnit.vw(24), gf.ScreenUnit.vw(24)))
READER_TOP_ACTIVE = pg.image.load("assets/img/eID/reader-top-active.png")
READER_TOP_ACTIVE = pg.transform.smoothscale(READER_TOP_ACTIVE, (gf.ScreenUnit.vw(24), gf.ScreenUnit.vw(24)))
card_state = cardReaderState.noCard
card_in_reader: bool = False

title_text = gf.Text("Login with your e-ID", gf.Font.customFont(int(gf.ScreenUnit.vw(5)), "assets/font/CasinoShadow.ttf"), (247, 228, 195))
subtitle_text = gf.Text("Insert with chip, pointing upwards", gf.Font.customFont(int(gf.ScreenUnit.vw(3)), "assets/font/CasinoShadow.ttf"), (247, 228, 195))
note_text = gf.Text("**We do not modify anything on your eID, the card is only read to verify your identity, give you a secure unique ID and verify your age. Your data is stored securely in a private database. For any concerns, please contact the owner**", gf.Font.H5, gf.Color.WHITE, italic=True)
name_text = gf.Text("", gf.Font.customFont(int(gf.ScreenUnit.vw(8)), "assets/font/CasinoShadow.ttf"), gf.Color.SPRING_GREEN)

create_account_button = gf.Button((gf.ScreenUnit.vw(50), gf.ScreenUnit.vh(10)), gf.Color.SPRING_GREEN, 8)
create_account_button.text("Create new account [A]", gf.Font.XLARGE, gf.Color.DARKMODE)
login_button = gf.Button((gf.ScreenUnit.vw(50), gf.ScreenUnit.vh(10)), gf.Color.SPRING_GREEN)
login_button.text("Login [A]", gf.Font.XLARGE, gf.Color.DARKMODE)
account_exists = False

def page():
    global SPECIMEN_FRONT, SPECIMEN_BACK, card_moving_up, card_move_up_animation, card_move_down_animation, specimen_back_rect, card_state, card_in_reader, account_exists
    data.APP.fill(gf.Color.BLACK)
    
    data.APP_SURFACE.blit(BG, (0, 0))
    if data.APP.drawElements():
        
        data.APP_SURFACE.blit(READER_BOTTOM, (gf.ScreenUnit.vw(3), gf.ScreenUnit.vh(100) - READER_BOTTOM.get_rect().height))
        
        if data.card_reader_state != card_state:
            card_state = data.card_reader_state
            if data.card_reader_state == cardReaderState.noCard:
                card_in_reader = False
                card_move_up_animation = MoveAnimation(gf.ScreenUnit.vh(30), gf.ScreenUnit.vh(5), 1)
            elif data.card_reader_state in [cardReaderState.cardInserted, cardReaderState.badRead, cardReaderState.succes]:
                if card_in_reader == False:
                    card_move_down_animation = MoveAnimation(gf.ScreenUnit.vh(5), gf.ScreenUnit.vh(30), 1)
                card_in_reader = True
                
        if card_state == cardReaderState.noCard:      
            if not card_move_up_animation.is_done():
                _, specimen_back_rect = card_move_up_animation.animate(SPECIMEN_BACK, specimen_back_rect)
        else:
            
            if not card_move_down_animation.is_done():
                _, specimen_back_rect = card_move_down_animation.animate(SPECIMEN_BACK, specimen_back_rect)
        data.APP_SURFACE.blit(SPECIMEN_BACK, (gf.ScreenUnit.vw(5), specimen_back_rect.y))
                
        if data.card_reader_state == cardReaderState.succes:
            data.APP_SURFACE.blit(READER_TOP_ACTIVE, (gf.ScreenUnit.vw(3), gf.ScreenUnit.vh(100) - READER_TOP_ACTIVE.get_rect().height))
        else:
            data.APP_SURFACE.blit(READER_TOP, (gf.ScreenUnit.vw(3), gf.ScreenUnit.vh(100) - READER_TOP.get_rect().height))
        
        if name_text.text == "" and data.card_data is not None:
            name_text.setText(f"Hello {data.card_data['firstName']}!")
            if backend.account_exists(data.card_data["rrn"]):
                account_exists = True
        elif name_text.text != "" and data.card_data is None:
            name_text.setText("")
            account_exists = False
            
        if name_text.text != "":
            name_text.place(gf.ScreenUnit.vw(40), gf.ScreenUnit.vh(25))
            if account_exists:
                login_button.place(gf.ScreenUnit.vw(40), gf.ScreenUnit.vh(75))
                
                if gf.Interactions.isKeyClicked(pg.K_a):
                    data.current_player = backend.get_account_info(data.card_data["rrn"])
                    data.current_player_id = data.card_data["rrn"]
                    data.active_page = pages.game
                
            else:
                create_account_button.place(gf.ScreenUnit.vw(40), gf.ScreenUnit.vh(75))
                if gf.Interactions.isKeyClicked(pg.K_a):
                    data.current_player = {
                        "id": data.card_data["rrn"],
                        "firstName": data.card_data["firstName"],
                        "birthdate": data.card_data["birthdate"]
                    }
                    data.current_player_id = data.card_data["rrn"]
                    data.active_page = pages.register

        title_text.place(gf.ScreenUnit.vw(40), gf.ScreenUnit.vh(5))
        subtitle_text.place(gf.ScreenUnit.vw(38), gf.ScreenUnit.vh(15))
        note_text.place(gf.ScreenUnit.vw(6), gf.ScreenUnit.vh(97))
        