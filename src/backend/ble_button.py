from src import data
from threading import Thread
import time

def start_input_handler():
    Thread(data.button_input.loop).start()

class BleButton_Handler:
    def __init__(self, debugger: bool = False):
        self.hit_button = BleButton(0)
        self.stand_button = BleButton(1)
        self.a_button = BleButton(2) # green
        self.b_button = BleButton(3) # red
        self.x_button = BleButton(4) # blue
        self.y_button = BleButton(5) # yellow
        self.debugging = debugger
        
    def any_clicked(self):
        return self.hit_button.is_clicked() or self.stand_button.is_clicked() or self.a_button.is_clicked() or self.b_button.is_clicked() or self.x_button.is_clicked() or self.y_button.is_clicked()
        
    def update(self):
        self.hit_button.update()
        self.stand_button.update()
        self.a_button.update()
        self.b_button.update()
        self.x_button.update()
        self.y_button.update()
        
    def loop(self):
        while data.running:
            self.update()
            if self.debugging:
                print("\033[6A\r", end="")
                print(self.hit_button, self.stand_button, self.a_button, self.b_button, self.x_button, self.y_button, sep="\n")
    
    
class BleButton:
    def __init__(self, pin):
        self.pin = pin
        self.flank: bool = False
        self.pressed: bool = False
        self.status_repr = "_" * 10
        self.press_start = None
        
        
    def __str__(self):
        return f"{self}: {self.status_repr}"
        
    def update(self, status: bool):
        if status:
            self.flank = False
            if not self.pressed:
                self.press_start = time.time()
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
    
    def is_held_for(self, time: float):
        return self.is_pressed() and time.time() - self.press_start > time