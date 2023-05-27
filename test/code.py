from pico import Pico
import board
from stepper import Stepper
import time
from screen import Screen
import digitalio
import neo
import errors
from config import *
import displayio
displayio.release_displays()


err = neo.Neo(pin=PIN_ERROR)

class Speedometer:
    def __init__(self):
        self.pico = Pico()
        self.i2c = Pico.i2c_create(sda=PIN_I2C_SDA, scl=PIN_I2C_SCL)
        self.speed = Stepper(i2c=self.i2c, address=MOTOR_ADDRESS)
        self.time_last_speed = time.monotonic_ns()//1_000_000
        self.time_last_rev = 0
        self.display = Screen(self.i2c)
        self.distance = 0
        self.last_update = 0
        self.wheel_sensor = Pico.button(PIN_MAGNETIC, digitalio.Pull.UP)

    def startup(self):
        self.speed.safe_start()
        self.speed.calibrate(PIN_LIGHT)

    def update(self):
        now = time.monotonic_ns()//1_000_000
        if now < self.last_update + 100:
            return
        self.last_update = now
        self.speed.goto_scaled(self._calculate_speed(), max_value=100)

        self.update_display()

    def _calculate_speed(self):
        # (circumference * m->km * ms->s / (now - last_update)
        # (circumference * 3.6 * 1000) / (now - last_update)
        s = int((2.6 * 3.6 * 1000) / (self.last_update - self.time_last_speed))
        return s

    def update_display(self):
        self.display.set_digit(self.distance)

    def spin(self):
        self.distance += 0.002
        self.time_last_speed = time.monotonic_ns()//1_000_000

    def run(self):
        while True:
            if self.wheel_sensor.value == False:
                self.spin()
                while self.wheel_sensor.value == False:
                    pass
            time.sleep(0.001)
            self.update()


def main():
    speedo = Speedometer()
    speedo.startup()
    while True:
        try:
            speedo.run()
        except Exception:
                pass


if __name__ == '__main__':
    err.fill(errors.NONE)
    try:
        main()
    except RuntimeError as re:
        print(re)
        if str(re) == 'No pull up found on SDA or SCL; check your wiring':
            err.fill(errors.NO_I2C) # yellow
        else:
            err.fill(errors.RUNTIME_ERROR) # cyan
    except ValueError as ve:
        print(ve)
        if str(ve) == 'No I2C device at address: 0x3c':
            err.fill(errors.NO_SCREEN) # red
        else:
            err.fill(errors.VALUE_ERROR) # green
    except OSError as ose:
        print(ose)
        if str(ose) == '[Errno 19] No such device':
            err.fill(errors.NO_MOTOR) # purple
        else:
            err.fill(errors.OS_ERROR) # blue

