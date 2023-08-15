from pico import Pico
import board
import time
import displayio
import neo
from config import *
from memory import Memory
import analogio
import digitalio


displayio.release_displays()
add = Pico.i2c_scanner(sda=board.GP0, scl=board.GP1)
for a in add:
    print(a)
# 
# mem = Memory(Pico.i2c_create(sda=PIN_I2C_SDA, scl=PIN_I2C_SCL), PIN_WP_MEMORY)
# 
# mem.write_distances(500.0, 10.0)
# 
# print(mem.read_distances())


with analogio.AnalogIn(PIN_LIGHT) as adc:
    while True:
        print(adc.value)
        time.sleep(0.1)

# wheel_sensor = Pico.button(PIN_MAGNETIC, digitalio.Pull.UP)
# while True:
#     print(wheel_sensor.value)
#     time.sleep(0.1)

# trip_button = Pico.button(PIN_RESET)
# 
# while True:
#     print(trip_button.value)
#     time.sleep(0.1)


# neo_lights = neo.Neo(pin=PIN_LIGHT)
# neo_lights.fill(LIGHT_BRIGHT)