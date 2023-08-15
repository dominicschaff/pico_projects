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
import analogio

displayio.release_displays()

err = neo.Neo(pin=PIN_ERROR)

class Speedometer:
    def __init__(self):
        self.pico = Pico()
        self.i2c = Pico.i2c_create(sda=PIN_I2C_SDA, scl=PIN_I2C_SCL)
        self.speed = Stepper(i2c=self.i2c, address=MOTOR_ADDRESS)
        self.last_update = 0
        self.time_last_rev = 0
        self.wheel_sensor = Pico.button(PIN_MAGNETIC, digitalio.Pull.UP)
        self.neo_lights = neo.Neo(pin=PIN_LIGHT_NEO, brightness=1.0)
        self.pin_light_dim = analogio.AnalogIn(PIN_LIGHT_DIMS)
        self.pin_light_bright = analogio.AnalogIn(PIN_LIGHT_BRIGHTS)

    def startup(self):
        self.speed.safe_start()
        self.speed.calibrate(PIN_LIGHT)

    def update(self):
        now = time.monotonic_ns()//1_000
        if now < self.last_update + UPDATE_INTERVAL:
            return
        print("Update")
        self.last_update = now
        s = self._calculate_speed()
        print(s)
        self.speed.goto_scaled(s, max_value=4000)

    def _calculate_speed(self):
        s = 16666 / (self.last_update - self.time_last_rev)
        return int(s)

    def spin(self):
        print("spin")
        self.time_last_rev = time.monotonic_ns()//1_000

    def run(self):
        while True:
            # Normal Use
            if self.wheel_sensor.value == False:
                self.spin()
                while self.wheel_sensor.value == False:
                    pass
            self.update()
            if self.pin_light_dim.value > 32_000:
                self.neo_lights.fill(LIGHT_DIMS)
            elif self.pin_light_bright.value > 32_000:
                self.neo_lights.fill(LIGHT_BRIGHT)
            else:
                self.neo_lights.fill((0,0,0))

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

