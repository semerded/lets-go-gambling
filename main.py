#!!  do not format

import gFrame as gf
from src import data
from gFrame import vars
from src.enums import pages
from pygame import K_ESCAPE
from src.backend import backend

# 200 doesn't matter and is overwritten on the line below
data.APP = gf.AppConstructor(data.APP_WIDTH, 800)
gf.Display.setAspectRatio(gf.aspectRatios.ratio16to9, data.APP_WIDTH)

# needs to be imported after gFrame is initialized
from src.frontend.frontend import page

data.APP_SURFACE = vars.mainDisplay

page_listing = [None, None, None, page, None]



if __name__ == "__main__":
    while data.running:
        data.APP.eventHandler(60)
        
        if gf.Interactions.isKeyReleased(K_ESCAPE):
            data.running = False
        
        page_listing[data.active_page.value]()  