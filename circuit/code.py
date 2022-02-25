import board
import digitalio
from time import sleep
import usb_hid
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.mouse import Mouse

LED = digitalio.DigitalInOut(board.GP25)
LED.direction = digitalio.Direction.OUTPUT

button1 = digitalio.DigitalInOut(board.GP16)
button1.switch_to_input(pull=digitalio.Pull.DOWN)

kbd = Keyboard(usb_hid.devices)
mouse = Mouse(usb_hid.devices)

while True:
    if button1.value:
        while button1.value:
            sleep(0.1)
        LED.value = True
        
        while not button1.value:
            mouse.click(Mouse.LEFT_BUTTON)
            sleep(0.05)
        while button1.value:
            sleep(0.1)
        LED.value = False