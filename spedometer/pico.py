import board
import digitalio
import time
import microcontroller
import busio
import analogio


class Pico:
    def __init__(self, buttons_pins=[], led_pin=board.GP25):
        self.light = Pico.led(led_pin)

        self.buttons = []
        for pin in buttons_pins:
            self.buttons.append(Pico.button(pin=pin))

    @staticmethod
    def button(pin, pull=digitalio.Pull.DOWN):
        b = digitalio.DigitalInOut(pin)
        b.switch_to_input(pull=pull)
        return b

    @staticmethod
    def adc(pin):
        return analogio.AnalogIn(pin)

    @staticmethod
    def led(pin=board.GP25):
        LED = digitalio.DigitalInOut(pin)
        LED.direction = digitalio.Direction.OUTPUT
        return LED

    @staticmethod
    def i2c_create(sda=board.GP0, scl=board.GP1):
        return busio.I2C(scl, sda)

    @staticmethod
    def i2c_scanner(sda=None, scl=None, i2c=None):
        if i2c is None:
            i2c = Pico.i2c_create(scl=scl, sda=sda)
        while not i2c.try_lock():
            pass
        addresses = [hex(device_address) for device_address in i2c.scan()]
        i2c.unlock()
        return addresses

    @staticmethod
    def flash(led, duration=0.1):
        led.value = True
        time.sleep(duration)
        led.value = False

    @staticmethod
    def temp():
        return microcontroller.cpu.temperature

    def b(self, button=0):
        return self.button_check(self.buttons[button])

    def button_wait(self, button=0):
        while not self.b(button):
            time.sleep(0.05)

    def button_check(self, button):
        if button.value is True:
            while button.value is True:
                time.sleep(0.1)
            return True
        return False

    def led_on(self):
        self.light.value = True

    def led_off(self):
        self.light.value = False

    def __enter__(self):
        self.led_on()
    def __exit__(self, v1, v2, v3):
        self.led_off()

if __name__ == '__main__':
    i2c = Pico.i2c_create()
    print("Addresses:")
    for address in Pico.i2c_scanner(i2c=i2c):
        print(address)