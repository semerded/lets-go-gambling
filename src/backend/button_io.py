import wiringpi
from src import data
from threading import Thread

def start_input_handler():
    Thread(data.button_input.loop).start()

class ButtonInput_Handler:
    def __init__(self, debugger: bool = False):
        self.hit_button = ButtonI(0)
        self.stand_button = ButtonI(1)
        self.a_button = ButtonI(2) # green
        self.b_button = ButtonI(3) # red
        self.x_button = ButtonI(4) # blue
        self.y_button = ButtonI(5) # yellow
        self.debugging = debugger
        
    def any_clicked(self):
        return self.hit_button.is_clicked() or self.stand_button.is_clicked() or self.a_button.is_clicked() or self.b_button.is_clicked() or self.x_button.is_clicked() or self.y_button.is_clicked()
        
    def read(self):
        self.hit_button.read()
        self.stand_button.read()
        self.a_button.read()
        self.b_button.read()
        self.x_button.read()
        self.y_button.read()
        
    def loop(self):
        while data.running:
            self.read()
            if self.debugging:
                print("\033[6A\r", end="")
                print(self.hit_button, self.stand_button, self.a_button, self.b_button, self.x_button, self.y_button, sep="\n")
    
    
class ButtonI:
    def __init__(self, pin):
        self.pin = pin
        self.flank: bool = False
        self.pressed: bool = False
        self.status_repr = "_" * 10
        wiringpi.pinMode(self.pin, 0)
        
        
    def __str__(self):
        return f"{self}: {self.status_repr}"
        
    def read(self):
        if wiringpi.digitalRead(self.pin):
            self.flank = False
            if not self.pressed:
                self.flank = True
                self.status_repr = self.status_repr[1:] + "|"
            else:
                self.status_repr = self.status_repr[1:] + "—"
            self.pressed = True
            
        else:
            if self.pressed:
                self.status_repr = self.status_repr[1:] + "|"
                self.flank = True
            else:
                self.status_repr = self.status_repr[1:] + "_"
            self.pressed = False
            
            
        
    def is_clicked(self):
        return self.pressed and self.flank
    
    def is_pressed(self):
        return self.pressed and not self.flank
    
    def is_released(self):
        return not self.pressed and self.flank