from pico import Pico
import board
import time
import displayio
import neo
from config import *
from memory import Memory
import analogio
import digitalio
import supervisor


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


# with analogio.AnalogIn(PIN_LIGHT) as adc:
#     while True:
#         print(adc.value)
#         time.sleep(0.1)

wheel_sensor = Pico.button(PIN_MAGNETIC, digitalio.Pull.UP)

class Ticker:
    def __init__(self, seconds, diff=250):
        self.seconds = seconds
        self.diff = diff
        self.size = int(1000/250) * seconds
        self.ticks = [[0, 0] for i in range(self.size)]
    
    def check(self):
        current = supervisor.ticks_ms()
        check = current - self.diff
        if self.ticks[-1][0] < check:
            self.flip([current, 0])
    
    def flip(self, val):
        for i in range(self.size - 1):
            self.ticks[i] = self.ticks[i+1]
        self.ticks[-1] = val
    
    def tick(self):
        self.ticks[-1][1] += 1
    
    def sum(self):
        total = 0
        for tick in self.ticks:
            total += tick[1]
        return total
    
    def first_time(self):
        return self.ticks[0][0]
        
ticks = Ticker(3)
its = 0
while True:
    spin = False
    if wheel_sensor.value == False:
        while wheel_sensor.value == False:
            pass
        spin = True
    ticks.check()
    current = supervisor.ticks_ms()
        
    if spin:
        ticks.tick()
    its += 1
    if its > 500:
        its = 0
        c = ticks.sum()
        print("rotations: %d, %f"%( c, 1000*(c)/(current - ticks.first_time())))

# trip_button = Pico.button(PIN_RESET)
# 
# while True:
#     print(trip_button.value)
#     time.sleep(0.1)


# neo_lights = neo.Neo(pin=PIN_LIGHT)
# neo_lights.fill(LIGHT_BRIGHT)