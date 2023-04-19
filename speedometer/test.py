from pico import Pico
from screen import SSD1306_I2C
import time
import board
import digitalio

display = SSD1306_I2C(128, 32, Pico.i2c_create())
display.fill(0)
display.text("%.1f"%(500.1), 0, 0, 1, size=4)
display.show()

status_wheel = Pico.led(board.GP14)
status_loop = Pico.led(board.GP7)
status_display = Pico.led(board.GP8)
wheel_sensor = Pico.button(board.GP2, digitalio.Pull.UP)

status_wheel.value = True
time.sleep(0.5)
status_wheel.value = False
time.sleep(0.5)
status_loop.value = True
time.sleep(0.5)
status_loop.value = False
time.sleep(0.5)
status_display.value = True
time.sleep(0.5)
status_display.value = False

while True:
    if wheel_sensor.value == False:
        status_wheel.value = True
        while wheel_sensor.value == False:
            pass
        status_wheel.value = False
        
