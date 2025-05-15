import gFrame as gf
import pygame as pg
from src import data
from src.enums import pages
from src.backend import backend
from src.frontend.components.center_x import center_x


BG = pg.image.load("assets/img/eID/bg.jpg")
BG = pg.transform.smoothscale(BG, (gf.ScreenUnit.vw(100), gf.ScreenUnit.vh(100)))
BG.set_alpha(130)




font = gf.Font.customFont(int(gf.ScreenUnit.vw(5)), "assets/font/CasinoShadow.ttf")
text_1 = gf.Text(f"Hello {data.current_player.get('firstName')}", font, gf.Color.GOLD)
text_2 = gf.Text(f"Do you want to create a new account?", font, gf.Color.WHITE)
font = gf.Font.customFont(int(gf.ScreenUnit.vw(2)), "assets/font/CasinoShadow.ttf")
text_3  = gf.Text("Your data will be stored securely in a private database", font, gf.Color.WHITE)
text_3_2  = gf.Text("For any concerns, please contact the owner", font, gf.Color.WHITE)
text_4 = gf.Text("You will get 1000 chips to start with", font, gf.Color.WHITE)
text_4_2 = gf.Text("More chips can be provided by the owners", font, gf.Color.WHITE)

button_confirm = gf.Button((gf.ScreenUnit.vw(40), gf.ScreenUnit.vh(10)), gf.Color.SPRING_GREEN, 8)
button_cancel = gf.Button((gf.ScreenUnit.vw(40), gf.ScreenUnit.vh(10)), gf.Color.LAVA_RED, 8)
button_confirm.text("Confirm [A]", gf.Font.XLARGE, gf.Color.DARKMODE)
button_cancel.text("Cancel [B]", gf.Font.XLARGE, gf.Color.DARKMODE)

def page():
    text_1.setText(f"Hello {data.current_player.get('firstName')}")
    data.APP.fill(gf.Color.BLACK)
    data.APP_SURFACE.blit(BG, (0, 0))
    text_1.place(center_x(text_1), gf.ScreenUnit.vh(20))
    text_2.place(center_x(text_2), gf.ScreenUnit.vh(27))
    text_3.place(center_x(text_3), gf.ScreenUnit.vh(40))
    text_3_2.place(center_x(text_3_2), gf.ScreenUnit.vh(44))
    
    text_4.place(center_x(text_4), gf.ScreenUnit.vh(50))
    text_4_2.place(center_x(text_4_2), gf.ScreenUnit.vh(54))
    
    button_confirm.place(gf.ScreenUnit.vw(5), gf.ScreenUnit.vh(70))
    button_cancel.place(gf.ScreenUnit.vw(55), gf.ScreenUnit.vh(70))
    
    if button_confirm.isClicked() or gf.Interactions.isKeyClicked(pg.K_a) or data.phys_buttons.a_button.is_clicked():
        backend.create_new_player(data.current_player.get("id"), data.current_player.get("firstName"), data.current_player.get("birthdate"))
        data.active_page = pages.start
    if button_cancel.isClicked() or gf.Interactions.isKeyClicked(pg.K_b) or data.phys_buttons.b_button.is_clicked():
        data.active_page = pages.idle