import time
from mylib import Leds, Colours, xrange, Button
from selfie import Selfie

selfie = Selfie(led_pin=28, led_count=24)

def mode_up(pin):
    global selfie
    print("mode_up")
    selfie.mode_next()

def mode_down(pin):
    global selfie
    print("mode_down")
    selfie.mode_previous()

def b1_up(pin):
    global selfie
    print("b1_up")
    selfie.b1_up()

def b1_down(pin):
    global selfie
    print("b1_down")
    selfie.b1_down()

def b2_up(pin):
    global selfie
    print("b2_up")
    selfie.b2_up()

def b2_down(pin):
    global selfie
    print("b2_down")
    selfie.b2_down()

def b3_up(pin):
    global selfie
    print("b3_up")
    selfie.b3_up()

def b3_down(pin):
    global selfie
    print("b3_down")
    selfie.b3_down()

Button(5).interupt(mode_up)
Button(0).interupt(mode_down)

Button(7).interupt(b1_up)
Button(6).interupt(b1_down)

Button(3).interupt(b2_up)
Button(1).interupt(b2_down)

Button(2).interupt(b3_up)
Button(4).interupt(b3_down)

while True:
    selfie.run()
    time.sleep(0.05)
        
    

