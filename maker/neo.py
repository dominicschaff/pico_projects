import time
import board
import neopixel

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (50, 50, 50)


class Neo:
    def __init__(self, pin=board.GP28, count=1):
        self.count = count
        self.pixels = neopixel.NeoPixel(pin, count, brightness=0.2, auto_write=False)
    def send(self, colour):
        neopixel_write(self.pin, colour)
        
        
    def wheel(self, pos):
        # Input a value 0 to 255 to get a color value.
        # The colours are a transition r - g - b - back to r.
        if pos < 0 or pos > 255:
            return (0, 0, 0)
        if pos < 85:
            return (255 - pos * 3, pos * 3, 0)
        if pos < 170:
            pos -= 85
            return (0, 255 - pos * 3, pos * 3)
        pos -= 170
        return (pos * 3, 0, 255 - pos * 3)
    
    def color_chase(self, color, wait):
        for i in range(self.count):
            self.pixels[i] = color
            time.sleep(wait)
            self.pixels.show()
        time.sleep(0.5)


    def rainbow_cycle(self, wait):
        for j in range(255):
            for i in range(self.count):
                rc_index = (i * 256 // self.count) + j
                self.pixels[i] = self.wheel(rc_index & 255)
            self.pixels.show()
            time.sleep(wait)
    
    def fill(self, colour):
        self.pixels.fill(colour)
        self.pixels.show()
    
    def show(self):
        self.pixels.show()

    

if __name__ == '__main__':
    n = Neo()
    n.fill(RED)
    time.sleep(1)  # Increase or decrease to change the speed of the solid color change.
    n.fill(GREEN)
    time.sleep(1)
    n.fill(BLUE)
    time.sleep(1)

    n.color_chase(RED, 0.5)  # Increase the number to slow down the color chase
    n.color_chase(YELLOW, 0.5)
    n.color_chase(GREEN, 0.5)
    n.color_chase(CYAN, 0.5)
    n.color_chase(BLUE, 0.5)
    n.color_chase(PURPLE, 0.5)

    n.rainbow_cycle(0.03)  # Increase the number to slow down the rainbow
    time.sleep(1)
