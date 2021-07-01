import time
from mylib import Leds, Colours, xrange, Button
from selfie import Selfie

selfie = Selfie(led_count=12)

def mode_up(pin):
    global selfie
    selfie.mode_next()

def mode_down(pin):
    global selfie
    selfie.mode_previous()

def b1_up(pin):
    global selfie
    selfie.b1_up()

def b1_down(pin):
    global selfie
    selfie.b1_down()

def b2_up(pin):
    global selfie
    selfie.b2_up()

def b2_down(pin):
    global selfie
    selfie.b2_down()

def b3_up(pin):
    global selfie
    selfie.b3_up()

def b3_down(pin):
    global selfie
    selfie.b3_down()

Button(3).interupt(mode_up)
Button(7).interupt(mode_down)
Button(0).interupt(b1_up)
Button(4).interupt(b1_down)
Button(1).interupt(b2_up)
Button(5).interupt(b2_down)
Button(2).interupt(b3_up)
Button(6).interupt(b3_down)

while True:
    selfie.run()
    time.sleep(0.1)
        
    

