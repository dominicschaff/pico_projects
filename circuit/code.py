from maker import Maker
import board
import time

m = Maker()


LEDS = [m.led(board.GP1), m.led(board.GP2), m.led(board.GP3)]
            
while True:

    if m.b1():
        print("b1")
        m.flash(LEDS[0])
        m.play_mario()

    elif m.b2():
        print("b2")
        m.flash(LEDS[1])

    elif m.b3():
        print("b3")
        m.flash(LEDS[2])
    time.sleep(0.1)
