# -*- coding: utf-8 -*-
# Modified for Raspberry Pi Pico with MicroPython
# Using SoftI2C with proper initialization delays
# Original code by Denis Pleic (DenisFromHR)

from machine import Pin, SoftI2C
from time import sleep_us, sleep_ms

# Default I2C pins for Pico (you can change these)
SDA_PIN = 4  # GP4
SCL_PIN = 5  # GP5

# LCD Address (common for most I2C LCDs)
ADDRESS = 0x27

class i2c_device:
    def __init__(self, addr, sda=SDA_PIN, scl=SCL_PIN, freq=100000):
        self.addr = addr
        self.i2c = SoftI2C(sda=Pin(sda), scl=Pin(scl), freq=freq)
        sleep_ms(100)  # Delay after I2C initialization

    # Write a single command
    def write_cmd(self, cmd):
        self.i2c.writeto(self.addr, bytearray([cmd]))
        sleep_us(100)  # Reduced from original 1000us

    # Write a command and argument
    def write_cmd_arg(self, cmd, data):
        self.i2c.writeto(self.addr, bytearray([cmd, data]))
        sleep_us(100)

    # Write a block of data
    def write_block_data(self, cmd, data):
        self.i2c.writeto(self.addr, bytearray([cmd] + data))
        sleep_us(100)

    # Read a single byte
    def read(self):
        return self.i2c.readfrom(self.addr, 1)[0]

    # Read data from command
    def read_data(self, cmd):
        return self.i2c.readfrom_mem(self.addr, cmd, 1)[0]

    # Read a block of data
    def read_block_data(self, cmd):
        return self.i2c.readfrom_mem(self.addr, cmd, 16)

# LCD commands and constants (unchanged from original)
LCD_CLEARDISPLAY = 0x01
LCD_RETURNHOME = 0x02
LCD_ENTRYMODESET = 0x04
LCD_DISPLAYCONTROL = 0x08
LCD_CURSORSHIFT = 0x10
LCD_FUNCTIONSET = 0x20
LCD_SETCGRAMADDR = 0x40
LCD_SETDDRAMADDR = 0x80

# Flags for display entry mode
LCD_ENTRYRIGHT = 0x00
LCD_ENTRYLEFT = 0x02
LCD_ENTRYSHIFTINCREMENT = 0x01
LCD_ENTRYSHIFTDECREMENT = 0x00

# Flags for display on/off control
LCD_DISPLAYON = 0x04
LCD_DISPLAYOFF = 0x00
LCD_CURSORON = 0x02
LCD_CURSOROFF = 0x00
LCD_BLINKON = 0x01
LCD_BLINKOFF = 0x00

# Flags for display/cursor shift
LCD_DISPLAYMOVE = 0x08
LCD_CURSORMOVE = 0x00
LCD_MOVERIGHT = 0x04
LCD_MOVELEFT = 0x00

# Flags for function set
LCD_8BITMODE = 0x10
LCD_4BITMODE = 0x00
LCD_2LINE = 0x08
LCD_1LINE = 0x00
LCD_5x10DOTS = 0x04
LCD_5x8DOTS = 0x00

# Flags for backlight control
LCD_BACKLIGHT = 0x08
LCD_NOBACKLIGHT = 0x00

En = 0b00000100  # Enable bit
Rw = 0b00000010  # Read/Write bit
Rs = 0b00000001  # Register select bit

class Lcd:
    def __init__(self, sda=SDA_PIN, scl=SCL_PIN):
        self.lcd_device = i2c_device(ADDRESS, sda, scl)
        sleep_ms(50)  # Additional delay after device creation
        
        # Initialize display with proper delays
        self.lcd_write(0x03)
        sleep_ms(5)  # Extended delay for first command
        self.lcd_write(0x03)
        sleep_ms(1)
        self.lcd_write(0x03)
        sleep_ms(1)
        self.lcd_write(0x02)  # Set to 4-bit mode
        sleep_ms(1)

        # Configure display with delays between commands
        self.lcd_write(LCD_FUNCTIONSET | LCD_2LINE | LCD_5x8DOTS | LCD_4BITMODE)
        sleep_ms(1)
        self.lcd_write(LCD_DISPLAYCONTROL | LCD_DISPLAYON)
        sleep_ms(1)
        self.lcd_write(LCD_CLEARDISPLAY)
        sleep_ms(5)  # Clear display needs more time
        self.lcd_write(LCD_ENTRYMODESET | LCD_ENTRYLEFT)
        sleep_ms(1)

    def lcd_strobe(self, data):
        self.lcd_device.write_cmd(data | En | LCD_BACKLIGHT)
        sleep_us(500)
        self.lcd_device.write_cmd(((data & ~En) | LCD_BACKLIGHT))
        sleep_us(100)

    def lcd_write_four_bits(self, data):
        self.lcd_device.write_cmd(data | LCD_BACKLIGHT)
        self.lcd_strobe(data)

    def lcd_write(self, cmd, mode=0):
        self.lcd_write_four_bits(mode | (cmd & 0xF0))
        self.lcd_write_four_bits(mode | ((cmd << 4) & 0xF0))

    def lcd_write_char(self, charvalue, mode=1):
        self.lcd_write_four_bits(mode | (charvalue & 0xF0))
        self.lcd_write_four_bits(mode | ((charvalue << 4) & 0xF0))

    def lcd_display_string(self, string, line=1, pos=0):
        if line == 1:
            pos_new = pos
        elif line == 2:
            pos_new = 0x40 + pos
        elif line == 3:
            pos_new = 0x14 + pos
        elif line == 4:
            pos_new = 0x54 + pos

        self.lcd_write(0x80 + pos_new)

        for char in string:
            self.lcd_write(ord(char), Rs)
            sleep_us(100)  # Small delay between characters

    def lcd_clear(self):
        self.lcd_write(LCD_CLEARDISPLAY)
        sleep_ms(5)  # Clear needs extra time
        self.lcd_write(LCD_RETURNHOME)
        sleep_ms(2)

    def backlight(self, state):
        if state == 1:
            self.lcd_device.write_cmd(LCD_BACKLIGHT)
        elif state == 0:
            self.lcd_device.write_cmd(LCD_NOBACKLIGHT)
        sleep_ms(1)

    def lcd_load_custom_chars(self, fontdata):
        self.lcd_write(0x40)
        sleep_us(100)
        for char in fontdata:
            for line in char:
                self.lcd_write_char(line)
                sleep_us(100)