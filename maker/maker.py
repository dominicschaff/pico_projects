from sd import SD
from sound import MARIO, Audio
from neo import Neo
import board
import digitalio
import time
import microcontroller
import time

import usb_hid
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.mouse import Mouse

class Maker:
    def __init__(self):
        self.sd = SD()
        self.audio = Audio()
        self.neo = Neo()
        
        self.button1 = digitalio.DigitalInOut(board.GP20)
        self.button1.switch_to_input(pull=digitalio.Pull.UP)
        self.button2 = digitalio.DigitalInOut(board.GP21)
        self.button2.switch_to_input(pull=digitalio.Pull.UP)
        self.button3 = digitalio.DigitalInOut(board.GP22)
        self.button3.switch_to_input(pull=digitalio.Pull.UP)
        
        self.kbd = Keyboard(usb_hid.devices)
        self.mouse = Mouse(usb_hid.devices)
    
    def b1(self):
        return self.button_check(self.button1)
    def b2(self):
        return self.button_check(self.button2)
    def b3(self):
        return self.button_check(self.button3)
    
    def button_check(self, button):
        if button.value == False:
            while button.value == False:
                time.sleep(0.1)
            return True
        return False
    
    def led(self, pin):
        LED = digitalio.DigitalInOut(pin)
        LED.direction = digitalio.Direction.OUTPUT
        return LED
    def flash(self, led, duration=0.1):
        led.value = True
        time.sleep(duration)
        led.value = False
    
    def play_mario(self):
        self.audio.buzzer_init()
        self.audio.play_song(MARIO)
        self.audio.buzzer.deinit()
    
    def temp(self):
        return microcontroller.cpu.temperature
    
    def keys_slow(self, keys, duration=0.1):
        # Example:
        # keys_slow([Keycode.WINDOWS, Keycode.S, Keycode.L, Keycode.A, Keycode.C, Keycode.K, Keycode.RETURN])
        for key in keys:
            self.kbd.send(key)
            time.sleep(duration)
        time.sleep(duration)
    
    def mouse_move(self, x, y, wheel=0):
        self.mouse.move(x=x, y=y, wheel=wheel)
    
    def mouse_left(self):
        self.mouse.click(Mouse.LEFT_BUTTON)
    
    def mouse_right(self):
        self.mouse.click(Mouse.RIGHT_BUTTON)
    
    def mouse_left_fast(self, count):
        for i in range(count):
            self.mouse.click(Mouse.LEFT_BUTTON)
            time.sleep(0.05)
        
