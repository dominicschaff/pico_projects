from pico import Pico
import board
from stepper import Stepper
import time
from screen import SSD1306_I2C
import digitalio
import neo
import errors


err = neo.Neo(pin=board.GP16)
signal = neo.Neo(pin=board.GP3, count=12)

class Speedometer:
    def __init__(self):
        self.pico = Pico()
        self.i2c = Pico.i2c_create()
        self.speed = Stepper(i2c=self.i2c, address=0xe)
        self.time_last_speed = time.monotonic_ns()//1_000_000
        self.time_last_rev = 0
        self.display = SSD1306_I2C(128, 32, self.i2c)
        self.distance = 0
        self.last_update = 0
        self.wheel_sensor = Pico.button(board.GP2, digitalio.Pull.UP)
        self.status_wheel = Pico.led(board.GP14)
        self.status_startup = Pico.led(board.GP7)
        self.status_display = Pico.led(board.GP8)

    def startup(self):
        self.status_startup.value = True
        self.speed.safe_start()
        self.speed.calibrate(board.A0)
        self.status_startup.value = False

    def update(self):
        now = time.monotonic_ns()//1_000_000
        if now < self.last_update + 100:
            return
        self.status_display.value = True
        self.last_update = now
        self.speed.goto_scaled(self._calculate_speed(), max_value=100)

        self.update_display()
        self.status_display.value = False

    def _calculate_speed(self):
        # (circumference * m->km * ms->s / (now - last_update)
        # (circumference * 3.6 * 1000) / (now - last_update)
        s = int((2.6 * 3.6 * 1000) / (self.last_update - self.time_last_speed))
        return s

    def update_display(self):
        self.display.fill(0)
        self.display.text("%05.0f"%(self.distance), 0, 0, 1, size=4)
        self.display.show()

    def spin(self):
        self.distance += 0.002
        self.time_last_speed = time.monotonic_ns()//1_000_000

    def run(self):
        while True:
            if self.wheel_sensor.value == False:
                self.status_wheel.value = True
                self.spin()
                while self.wheel_sensor.value == False:
                    pass
                self.status_wheel.value = False
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
    signal.rainbow()
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

