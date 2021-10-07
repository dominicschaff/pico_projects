###  This example code uses: Maker Pi Pico ;; Reference: www.cytron.io/p-maker-pi-pico

import time
from maker import Maker
import board

m = Maker()

import usb_hid
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.mouse import Mouse

# Set up keyboard and mouse.
kbd = Keyboard(usb_hid.devices)
mouse = Mouse(usb_hid.devices)
direction = True

def send_wait(keys, wait=0.1):
    for key in keys:
        kbd.send(key)
        time.sleep(wait)
    time.sleep(wait)

while True:
    if m.b1():
#         kbd.send(Keycode.LEFT_CONTROL, Keycode.LEFT_ALT, Keycode.RIGHT_ARROW)
        send_wait([Keycode.WINDOWS, Keycode.S, Keycode.L, Keycode.A, Keycode.C, Keycode.K, Keycode.RETURN])
        send_wait([Keycode.WINDOWS, Keycode.G, Keycode.E, Keycode.A, Keycode.R, Keycode.Y, Keycode.RETURN])
        
    if m.b2():
        for i in range(500):
            mouse.click(Mouse.LEFT_BUTTON)
            time.sleep(0.05)
        
    if m.b3():
        mouse.move(x=60)
        mouse.move(y=-25)
    time.sleep(0.1)
