import array, time
from machine import I2C, Pin
import rp2

def CreateI2C(sda=0, scl=1):
    return I2C(0,sda=Pin(sda), scl=Pin(scl))


def xrange(s, e, i):
    while s <= e:
        yield s
        s+=i


class Colours:
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    YELLOW = (255, 150, 0)
    GREEN = (0, 255, 0)
    CYAN = (0, 255, 255)
    BLUE = (0, 0, 255)
    PURPLE = (180, 0, 255)
    WHITE = (255, 255, 255)
    ALL_COLOURS = (RED, YELLOW, GREEN, CYAN, BLUE, PURPLE, WHITE)


@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    wrap_target()
    label("bitloop")
    out(x, 1)               .side(0)    [T3 - 1]
    jmp(not_x, "do_zero")   .side(1)    [T1 - 1]
    jmp("bitloop")          .side(1)    [T2 - 1]
    label("do_zero")
    nop()                   .side(0)    [T2 - 1]
    wrap()


class Leds():
    def __init__(self, pin=16, leds=1):
        self.pin = pin
        self.leds = leds
        self.sm = rp2.StateMachine(0, ws2812, freq=8_000_000, sideset_base=Pin(self.pin))
        self.sm.active(1)
        self.ar = array.array("I", [0 for _ in range(self.leds)])

    def show(self):
        dimmer_ar = array.array("I", [0 for _ in range(self.leds)])
        for i,c in enumerate(self.ar):
            r = (c >> 8) & 0xFF
            g = (c >> 16) & 0xFF
            b = c & 0xFF
            dimmer_ar[i] = (g<<16) + (r<<8) + b
        self.sm.put(dimmer_ar, 8)
        time.sleep_ms(10)

    def pixel(self, i, colour, brightness=0.1):
        self.ar[i] = (int(colour[1] * brightness)<<16) + (int(colour[0] * brightness)<<8) + int(colour[2] * brightness)

    def fill(self, colour, brightness=0.1):
        for i in range(self.leds):
            self.pixel(i, colour, brightness)


