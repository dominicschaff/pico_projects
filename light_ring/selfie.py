from mylib import Leds, Colours, xrange, Button

class Selfie:
    EMPTY = 0
    WHITE = 1
    RGB = 2
    FLIP = 3
    RAINBOW = 4
    BREATHE = 5

    def __init__(self, led_pin=16, led_count=1):
        self.led_count = led_count
        self.leds = Leds(pin=led_pin, leds=led_count)
        self.mode = Selfie.EMPTY
        self.brightness = 0.1
        self.iteration = 0
        self.colour = Colours.PURPLE
    
    def set_mode(self, mode):
        print("Setting mode to %d" % mode)
        self.mode = mode
        self.iteration = 0
    
    def mode_next(self):
        self.set_mode((self.mode+1)%6)
    
    def mode_previous(self):
        self.set_mode((self.mode+5)%6)
        
    def mode_breathe(self):
        if self.iteration > 100:
            self.iteration = 0

        s = self.iteration
        if self.iteration > 50:
            s = 100 - self.iteration
        self.leds.fill(self.colour, s/50)
        self.iteration += 1
        
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
    
    def mode_rainbow(self):
        for i in range(self.led_count):
            rc_index = (i * 256 // self.led_count) + self.iteration
            self.leds.pixel(i, self.wheel(rc_index & 255))
        self.iteration = (self.iteration + 1) & 256
    
    def run(self):
        if self.mode == Selfie.EMPTY:
            print("Show black")
            self.leds.fill(Colours.BLACK)
        if self.mode == Selfie.WHITE:
            print("Show white with %f" % self.brightness)
            self.leds.fill(Colours.WHITE, self.brightness)
        if self.mode == Selfie.RGB:
            print("Show RGB")
            pass
        if self.mode == Selfie.FLIP:
            print("Show Flip")
            pass
        if self.mode == Selfie.RAINBOW:
            print("Show Rainbow")
            self.mode_rainbow()
        if self.mode == Selfie.BREATHE:
            print("Breathing")
            self.mode_breathe()
        self.leds.show()
