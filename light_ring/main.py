import time
from mylib import Leds, Colours, xrange, Button
from selfie import Selfie
import _thread

global selfie
selfie = Selfie(led_count=2)

def selfie_render_thread():
    global selfie
    while True:
        selfie.run()
        time.sleep(0.1)

_thread.start_new_thread(selfie_render_thread, ())

def mode_up(pin):
    global selfie
    selfie.mode_next()

def mode_down(pin):
    global selfie
    selfie.mode_previous()

Button(14).interupt(mode_up)
Button(15).interupt(mode_down)

while True:
    time.sleep(1)
        
    

