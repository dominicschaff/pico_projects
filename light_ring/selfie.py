from mylib import Leds, Colours, xrange, Button

MAX_COLOUR = len(Colours.ALL_COLOURS)-1

class Selfie:
    EMPTY = 0
    WHITE = 1
    RGB = 2
    FLIP = 3
    RAINBOW = 4
    BREATHE = 5
    RAINBOW_BREATHE = 6

    def __init__(self, led_pin=16, led_count=1):
        self.led_count = led_count
        self.half = led_count//2
        self.leds = Leds(pin=led_pin, leds=led_count)
        self.mode = Selfie.EMPTY
        self.brightness = 0.1
        self.iteration = 0
        self.iteration_size = 1
        self.colour_index = 5
        self.colour_index2 = 5
        self.colour = Colours.ALL_COLOURS[self.colour_index]
        self.colour2 = Colours.ALL_COLOURS[self.colour_index2]
        self.white_index = Colours.WHITE_PURE

    def set_mode(self, mode):
        print("Setting mode to %d" % mode)
        self.mode = mode
        self.iteration = 0

    def mode_next(self):
        self.set_mode((self.mode + 1)%7)

    def mode_previous(self):
        self.set_mode((self.mode - 1 + 7)%7)

    def mode_breathe(self):
        self.leds.fill(self.colour, abs(self.iteration / 50))
        self.iteration = self.iteration + self.iteration_size
        if self.iteration > 50:
            self.iteration = -50

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

    def mode_rainbow_breathe(self):
        self.leds.fill(self.wheel(self.iteration & 255), self.brightness)
        self.iteration = (self.iteration + self.iteration_size) % 256

    def mode_flip(self):
        for i in range(self.half):
            self.leds.pixel(i, self.colour, self.brightness)
        for i in range(self.half, self.led_count):
            self.leds.pixel(i, self.colour2, self.brightness)

    def run(self):
        if self.mode == Selfie.EMPTY:
            self.leds.fill(Colours.BLACK)
        elif self.mode == Selfie.WHITE:
            self.leds.fill(Colours.WHITES[self.white_index], self.brightness)
        elif self.mode == Selfie.RGB:
            self.leds.fill(self.colour, 1.0)
        elif self.mode == Selfie.FLIP:
            self.mode_flip()
        elif self.mode == Selfie.RAINBOW:
            self.mode_rainbow()
        elif self.mode == Selfie.BREATHE:
            self.mode_breathe()
        elif self.mode == Selfie.RAINBOW_BREATHE:
            self.mode_rainbow_breathe()
        self.leds.show()

    def b1_up(self):
        if self.mode in [Selfie.WHITE, Selfie.RAINBOW, Selfie.FLIP, Selfie.RAINBOW_BREATHE]:
            self.brightness = min(1.0, self.brightness + 0.1)
        if self.mode == Selfie.BREATHE:
            self.colour_index = min(self.colour_index + 1, MAX_COLOUR)
            self.colour = Colours.ALL_COLOURS[self.colour_index]
        if self.mode == Selfie.RGB:
            self.colour[0] = min(self.colour[0] + 10, 255)

    def b1_down(self):
        if self.mode in [Selfie.WHITE, Selfie.RAINBOW, Selfie.FLIP, Selfie.RAINBOW_BREATHE]:
            self.brightness = max(0.0, self.brightness - 0.1)
        if self.mode == Selfie.BREATHE:
            self.colour_index = max(self.colour_index - 1, 0)
            self.colour = Colours.ALL_COLOURS[self.colour_index]
        if self.mode == Selfie.RGB:
            self.colour[0] = max(self.colour[0] - 10, 0)

    def b2_up(self):
        if self.mode == Selfie.RGB:
            self.colour[1] = min(self.colour[1] + 10, 255)
        if self.mode == Selfie.FLIP:
            self.colour_index = min(self.colour_index + 1, MAX_COLOUR)
            self.colour = Colours.ALL_COLOURS[self.colour_index]
        if self.mode in [Selfie.RAINBOW, Selfie.BREATHE, Selfie.RAINBOW_BREATHE]:
            self.iteration_size += 1
        if self.mode == Selfie.WHITE:
            self.white_index = min(self.white_index + 1, MAX_COLOUR)

    def b2_down(self):
        if self.mode == Selfie.RGB:
            self.colour[1] = max(self.colour[1] - 10, 0)
        if self.mode == Selfie.FLIP:
            self.colour_index = max(self.colour_index - 1, 0)
            self.colour = Colours.ALL_COLOURS[self.colour_index]
        if self.mode in [Selfie.RAINBOW, Selfie.BREATHE, Selfie.RAINBOW_BREATHE]:
            self.iteration_size -= 1
        if self.mode == Selfie.WHITE:
            self.white_index = max(0, self.white_index -1)

    def b3_up(self):
        if self.mode == Selfie.RGB:
            self.colour[2] = min(self.colour[2] + 10, 255)
        if self.mode == Selfie.FLIP:
            self.colour_index2 = min(self.colour_index2 + 1, MAX_COLOUR)
            self.colour2 = Colours.ALL_COLOURS[self.colour_index2]

    def b3_down(self):
        if self.mode == Selfie.RGB:
            self.colour[2] = max(self.colour[2] - 10, 0)
        if self.mode == Selfie.FLIP:
            self.colour_index2 = max(self.colour_index2 - 1, 0)
            self.colour2 = Colours.ALL_COLOURS[self.colour_index2]
