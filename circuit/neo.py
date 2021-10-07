from neopixel_write import neopixel_write
import board

class Neo:
    def __init__(self, pin=board.GP28):
        self.pin = pin
    def send(self, colour):
        neopixel_write(self.pin, colour)