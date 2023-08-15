from pico import Pico
from stepper import Stepper
import time
from screen import Screen
import digitalio
import neo
from config import *
import displayio
import json
from memory import Memory

displayio.release_displays()

err = neo.Neo(pin=PIN_ERROR)

class Speedometer:
    def __init__(self):
        self.pico = Pico()
        self.i2c = Pico.i2c_create(sda=PIN_I2C_SDA, scl=PIN_I2C_SCL)
        self.speed = Stepper(i2c=self.i2c, address=MOTOR_ADDRESS)
        self.time_last_speed = time.monotonic_ns()//1_000_000
        self.previous_distance = 0
        self.time_last_rev = 0
        self.display = Screen(self.i2c)
        self.distance = 0.0
        self.trip_meter = 0.0
        self.last_update = 0
        self.last_write = 0
        self.wheel_sensor = Pico.button(PIN_MAGNETIC, digitalio.Pull.UP)
        self.data = {}
        self.trip_button = Pico.button(PIN_RESET)
        self.display_total_distance = True
        self.memory = Memory(self.i2c, PIN_WP_MEMORY)
        #self.neo_lights = neo.Neo(pin=PIN_LIGHT_NEO)
        #self.pin_light_dim = Pico.button(PIN_LIGHT_DIMS)
        #self.pin_light_bright = Pico.button(PIN_LIGHT_BRIGHTS)

    def startup(self):
        self.speed.safe_start()
        self.speed.calibrate(PIN_LIGHT)
        self._read_data()
    
    def _read_data(self):
        self.distance, self.trip_meter = self.memory.read_distances()
        
    def _write_data(self):
        self.memory.write_distances(self.distance, self.trip_meter)

    def update(self):
        now = time.monotonic_ns()//1_000_000
        if now < self.last_update + UPDATE_INTERVAL:
            return
        print("Update")
        self.last_update = now
        s = self._calculate_speed()
        self.speed.goto_scaled(s, max_value=100)

        if self.display_total_distance:
            self.display.set_digit(self.distance)
        else:
            self.display.set_digit(self.trip_meter, tenths=True)
        
        if self.last_write + STATE_MINIMUM_DURATION < now:
            self.last_write = now
            self._write_data()

    def _calculate_speed(self):
        s = 1_000_000*(self.distance - self.previous_distance) / (self.last_update - self.time_last_speed)
        self.previous_distance = self.distance
        return int(s)

    def spin(self):
        print("spin")
        self.distance += WHEEL_SIZE
        self.time_last_speed = time.monotonic_ns()//1_000_000

    def run(self):
        while True:
            # Normal Use
            if self.wheel_sensor.value == False:
                self.spin()
                while self.wheel_sensor.value == False:
                    pass
            self.update()
            if self.trip_button.value == True:
                start = time.monotonic_ns()//1_000_000
                while self.trip_button.value == True:
                    pass
                end = time.monotonic_ns()//1_000_000
                if end - start < RESET_TIME:
                    self.display_total_distance = not self.display_total_distance
                else:
                    self.trip_meter = 0.0
                    self._write_data()
#             if self.pin_light_dim.value:
#                 if self.pin_light_bright.value:
#                     self.neo_lights.fill(LIGHT_BRIGHT)
#                 else:
#                     self.neo_lights.fill(LIGHT_DIMS)
                

def main():
    speedo = Speedometer()
    speedo.startup()
    print("running")
    while True:
        speedo.run()


if __name__ == '__main__':
    err.fill(ERR_NONE)
    try:
        main()
    except RuntimeError as re:
        print(re)
        if str(re) == 'No pull up found on SDA or SCL; check your wiring':
            err.fill(ERR_NO_I2C) # white
        elif str(re) == "Cannot remount '/' when visible via USB.":
            err.fill(ERR_NO_STORAGE) # orange
        else:
            err.fill(ERR_RUNTIME_ERROR) # cyan
    except ValueError as ve:
        print(ve)
        if str(ve) == 'No I2C device at address: 0x3c':
            err.fill(ERR_NO_SCREEN) # red
        else:
            err.fill(ERR_VALUE_ERROR) # green
    except OSError as ose:
        print(ose)
        if str(ose) == '[Errno 19] No such device':
            err.fill(ERR_NO_MOTOR) # purple
        else:
            err.fill(ERR_OS_ERROR) # blue

