from pico import Pico
import board
from stepper import Stepper
import time
from screen import SSD1306_I2C
import digitalio

class Speedometer:
    def __init__(self):
        self.pico = Pico()
        self.i2c = Pico.i2c_create()
        self.speed = Stepper(i2c=self.i2c, address=0xf)
        self.time_last_speed = time.monotonic_ns()//1_000_000
        self.time_last_rev = 0
        self.display = SSD1306_I2C(128, 32, self.i2c)
        self.distance = 0
        self.last_update = 0
        self.wheel_sensor = Pico.button(board.GP2, digitalio.Pull.UP)
    
    def startup(self):
        self.speed.safe_start()
        self.speed.calibrate(board.A0)
    
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
        self.display.fill(0)
        self.display.text("%.1f"%(self.distance), 0, 0, 1, size=4)
        self.display.show()
    
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
    main()
