from pico import Pico
import board
import time
import displayio
import neo
from config import *
from memory import Memory
import analogio

# displayio.release_displays()
# 
# mem = Memory(Pico.i2c_create(sda=PIN_I2C_SDA, scl=PIN_I2C_SCL), PIN_WP_MEMORY)
# 
# mem.write_distances(500.0, 10.0)
# 
# print(mem.read_distances())


# with analogio.AnalogIn(PIN_LIGHT) as adc:
#     while True:
#         print(adc.value)
#         time.sleep(0.2)


trip_button = Pico.button(PIN_RESET)

while True:
    print(trip_button.value)
    time.sleep(0.1)