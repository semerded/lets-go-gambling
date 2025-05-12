import gFrame as gf

def center_x(text: gf.Text):
    x = gf.ScreenUnit.vw(50) - (text.textWidth / 2)
    return x