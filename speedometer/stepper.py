import time
import board
import analogio
from random import randint


class Stepper:
    def __init__(self, i2c, address=0xe):
        self._i2c = i2c
        self._address = address
        self.start = self.position()
        self.end = self.position()
        self.last = None
        self.diff = 1

    def position(self):
        while not self._i2c.try_lock():
            pass
        self._i2c.writeto(self._address, bytes([0xA1, 0x22]))
        result = bytearray(4)
        self._i2c.readfrom_into(self._address, buffer=result, end=4)
        position = result[0] + (result[1] << 8) + (result[2] << 16) + (result[3] << 24)
        if position >= (1 << 31):
          position -= (1 << 32)
        self._i2c.unlock()
        return position

    def goto(self, target):
        if target == self.last:
#             print("Ignore change")
            return
        self.last = target
        print("GOTO: ", target)
        while not self._i2c.try_lock():
            pass
        command = [0xE0,
          target >> 0 & 0xFF,
          target >> 8 & 0xFF,
          target >> 16 & 0xFF,
          target >> 24 & 0xFF]
        self._i2c.writeto(self._address, bytes(command))
        self._i2c.unlock()

    def safe_start(self):
        while not self._i2c.try_lock():
            pass
        command = [0x83]
        self._i2c.writeto(self._address, bytes(command))
        self._i2c.unlock()

    def wait_till(self, target = 0):
        p =  self.position()
        while p < target-2 or p > target+2:
            time.sleep(0.1)
            print("Waiting", p, target)
            p =  self.position()

    def left(self, steps=1):
        self.goto(self.position() + steps)

    def right(self, steps=1):
        self.goto(self.position() - steps)

    def calibrate(self, pin, size=120, difference=8_000):
        print("Turn clockwise")
        self.right(50)
        time.sleep(0.5)
        with analogio.AnalogIn(pin) as adc:
            start = adc.value
            min_value = adc.value

            while True:
                print("Move Left")
                self.left()
                time.sleep(0.01)
                if adc.value > min_value and min_value < start - difference:
                    print("Hit Sensor")
                    break
                min_value = adc.value

        self.start = self.position()
        self.end = self.start - size
        self.diff = self.start - self.end
        if self.diff < 0 :
            self.diff = -self.diff

    def goto_scaled(self, value, max_value=100):
        self.goto(int(self.start - (min(value, max_value)/max_value) * self.diff))

if __name__ == '__main__':
    from pico import Pico
    pico = Pico()
    i1 = pico.i2c_create(sda=board.GP0, scl=board.GP1)

    speed = Stepper(i2c=i1, address=0xf)

    time.sleep(2)
    speed.safe_start()
    time.sleep(0.5)
    speed.calibrate(board.A0)
    while True:
        speed.goto_scaled(randint(0, 80), 100)
        time.sleep(0.1)
