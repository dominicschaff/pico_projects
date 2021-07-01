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
        self.iteration_size = 1
        self.colour_index = 5
        self.colour_index2 = 5
        self.colour = Colours.ALL_COLOURS[self.colour_index]
        self.colour2 = Colours.ALL_COLOURS[self.colour_index2]

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
            self.leds.pixel(i, self.wheel(rc_index & 255), self.brightness)
        self.iteration = (self.iteration + self.iteration_size) % 256

    def mode_flip(self):
        half = self.led_count//2
        for i in range(half):
            self.leds.pixel(i, self.colour, self.brightness)
        for i in range(half, self.led_count):
            self.leds.pixel(i, self.colour2, self.brightness)

    def run(self):
        if self.mode == Selfie.EMPTY:
            print("Show black")
            self.leds.fill(Colours.BLACK)
        if self.mode == Selfie.WHITE:
            print("Show white with %f" % self.brightness)
            self.leds.fill(Colours.WHITE, self.brightness)
        if self.mode == Selfie.RGB:
            print("Show RGB")
            self.leds.fill(self.colour, 1.0)
        if self.mode == Selfie.FLIP:
            print("Show Flip")
            self.mode_flip()
        if self.mode == Selfie.RAINBOW:
            print("Show Rainbow")
            self.mode_rainbow()
        if self.mode == Selfie.BREATHE:
            print("Breathing")
            self.mode_breathe()
        self.leds.show()

    def b1_up(self):
        if self.mode in [Selfie.WHITE, Selfie.RAINBOW, Selfie.FLIP]:
            self.brightness = min(1.0, self.brightness + 0.1)
        if self.mode == Selfie.BREATHE:
            self.colour_index = (self.colour_index + 1) % len(Colours.ALL_COLOURS)
            self.colour = Colours.ALL_COLOURS[self.colour_index]
        if self.mode == Selfie.RGB:
            self.colour[0] = min(self.colour[0] + 10, 255)

    def b1_down(self):
        if self.mode in [Selfie.WHITE, Selfie.RAINBOW, Selfie.FLIP]:
            self.brightness = max(0.0, self.brightness - 0.1)
        if self.mode == Selfie.BREATHE:
            self.colour_index = (self.colour_index - 1 + len(Colours.ALL_COLOURS)) % len(Colours.ALL_COLOURS)
            self.colour = Colours.ALL_COLOURS[self.colour_index]
        if self.mode == Selfie.RGB:
            self.colour[0] = max(self.colour[0] - 10, 0)

    def b2_up(self):
        if self.mode == Selfie.RGB:
            self.colour[1] = min(self.colour[1] + 10, 255)
        if self.mode == Selfie.FLIP:
            self.colour_index = (self.colour_index + 1) % len(Colours.ALL_COLOURS)
            self.colour = Colours.ALL_COLOURS[self.colour_index]
        if self.mode == Selfie.RAINBOW:
            self.iteration_size += 1

    def b2_down(self):
        if self.mode == Selfie.RGB:
            self.colour[1] = max(self.colour[1] - 10, 0)
        if self.mode == Selfie.FLIP:
            self.colour_index = (self.colour_index - 1 + len(Colours.ALL_COLOURS)) % len(Colours.ALL_COLOURS)
            self.colour = Colours.ALL_COLOURS[self.colour_index]
        if self.mode == Selfie.RAINBOW:
            self.iteration_size -= 1

    def b3_up(self):
        if self.mode == Selfie.RGB:
            self.colour[2] = min(self.colour[2] + 10, 255)
        if self.mode == Selfie.FLIP:
            self.colour_index2 = (self.colour_index2 + 1) % len(Colours.ALL_COLOURS)
            self.colour2 = Colours.ALL_COLOURS[self.colour_index2]

    def b3_down(self):
        if self.mode == Selfie.RGB:
            self.colour[2] = max(self.colour[2] - 10, 0)
        if self.mode == Selfie.FLIP:
            self.colour_index2 = (self.colour_index2 - 1 + len(Colours.ALL_COLOURS)) % len(Colours.ALL_COLOURS)
            self.colour2 = Colours.ALL_COLOURS[self.colour_index2]
