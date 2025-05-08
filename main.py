#!!  do not format

import gFrame as gf
from src import data
from gFrame import vars
from src.enums import pages
from pygame import K_ESCAPE
from src.backend import backend
from src.backend.eID.eID_handler import run_eid_thread, stop_eid_thread
import sys

# 200 doesn't matter and is overwritten on the line below
data.APP = gf.AppConstructor(data.APP_WIDTH, 800)
gf.Display.setAspectRatio(gf.aspectRatios.ratio16to9, data.APP_WIDTH)

# needs to be imported after gFrame is initialized
from src.frontend.pages.blackjack.blackjack_page import page as blackjack_page
from src.frontend.pages.eID.eID_page import page as eID_page
from src.frontend.pages.register.register_page import page as register_page

data.APP_SURFACE = vars.mainDisplay

page_listing = [None, eID_page, register_page, blackjack_page, None]

def exception_hook(exc_type, exc_value, exc_traceback):
    data.running = False
    if exc_type != KeyboardInterrupt:
        sys.__excepthook__(exc_type, exc_value, exc_traceback)

sys.excepthook = exception_hook

if __name__ == "__main__":
    while data.running:
        if data.active_page == pages.login and not data.card_reader_thread_running:
            run_eid_thread()
        elif data.active_page != pages.login and data.card_reader_thread_running:
            stop_eid_thread()
        
        data.APP.eventHandler(60)
        
        if gf.Interactions.isKeyReleased(K_ESCAPE):
            data.running = False
            
        page_listing[data.active_page.value]()  
        
        if data.debugging:
            fps = data.APP.clock.get_fps()
            gf.Text.simpleText(fps, 5, 5, color= gf.Color.GREEN)
            