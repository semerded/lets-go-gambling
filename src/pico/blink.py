from machine import Pin, PWM
import time

# Button Setup (GP1-GP6, internal pull-down enabled)
buttons = [
    Pin(1, Pin.IN, Pin.PULL_DOWN),  # Button 1 (GP1)
    Pin(2, Pin.IN, Pin.PULL_DOWN),  # Button 2 (GP2)
    Pin(3, Pin.IN, Pin.PULL_DOWN),  # Button 3 (GP3)
    Pin(4, Pin.IN, Pin.PULL_DOWN),  # Button 4 (GP4)
    Pin(5, Pin.IN, Pin.PULL_DOWN),  # Button 5 (GP5) - Has LED
    Pin(6, Pin.IN, Pin.PULL_DOWN)   # Button 6 (GP6) - Has LED
]

# PWM LED Setup (GP16 and GP17)
leds = [
    PWM(Pin(16)),  # LED for Button 5 (GP16)
    PWM(Pin(17))   # LED for Button 6 (GP17)
]
for led in leds:
    led.freq(1000)  # Set PWM frequency to 1kHz

# Test all buttons and LEDs
print("Starting test... Press any button.")
print("Buttons 5-6 will light their LEDs when pressed.")

while True:
    # Check each button
    for i in range(6):
        if buttons[i].value():
            print(f"Button {i+1} pressed!")
            
            # Light corresponding LED for Buttons 5-6
            if i == 4:  # Button 5
                leds[0].duty_u16(32768)  # 50% brightness
            elif i == 5:  # Button 6
                leds[1].duty_u16(65535)  # 100% brightness
                
            time.sleep_ms(300)  # Simple debounce
    
    # Turn off LEDs when buttons are released
    if not buttons[4].value():
        leds[0].duty_u16(0)
    if not buttons[5].value():
        leds[1].duty_u16(0)
    
    time.sleep_ms(50)  # Reduce CPU usage