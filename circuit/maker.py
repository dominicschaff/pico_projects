from sd import SD
from sound import MARIO, Audio
from neo import Neo
import board
import digitalio
import time

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
