from screen import Screen
from lcd import BLACK, WHITE, CYAN, PURPLE, BLUE
from random import randrange
from PiicoDev_MS5637 import PiicoDev_MS5637
import time

class Weather:
    def __init__(self, graph_every=10):
        self.screen = Screen()
        self.temps = []
        self.humids = []
        self.baroms = []
        self.temp = 0
        self.humid = 0
        self.barom = 0
        self.last = 0
        self.graph_every = graph_every
        self.voltage = 0
        self.percentage = 0
        self.width = self.screen.lcd.width

    def update(self):
        self.screen.clear()
        self.screen.rect_fill(0, 0, 160, 10, BLACK)
        self.screen.text("%.1fV" % self.voltage, 0, 1, WHITE)
#         self.screen.text_center("%d" % time.localtime(), self.screen.lcd.width//2, 5, WHITE)
        self.screen.text_right("%.0f%%"%self.percentage, self.screen.lcd.width, 5, WHITE)
        
        top_y = 19
        first = 25
        second = 80
        third = 135
        box_width = 50
        half_x =  self.screen.lcd.width//2

        self.screen.text_center("%.1f" % self.temp, first, top_y, BLACK)
        self.screen.text_center("%.0f%%" % self.humid, second, top_y, BLACK)
        self.screen.text_center("%.0f" % self.barom, third, top_y, BLACK)

        self.screen.rect(first-25, top_y - 8, box_width, 16, BLACK)
        self.screen.rect(second-25, top_y - 8, box_width, 16, BLACK)
        self.screen.rect(third-25, top_y - 8, box_width, 16, BLACK)
        
        self.screen.graph("Temperature", self.temps, half_x, 45, 32, self.width)

        self.screen.graph("Humidity", self.humids, half_x, 78, 32, self.width)
        
        self.screen.graph("Barometer", self.baroms, half_x, 111, 32, self.width)
        self.screen.show()

    def vals(self, temp, humid, barom):
        print("Set: temp:%.1f | humid:%.1f" % (temp, humid))
        self.temp = temp
        self.humid = humid
        self.barom = barom
        self.last -= 1
        if self.last <= 1:
            self.last = self.graph_every
            self.temps.append(self.temp)
            self.humids.append(self.humid)
            self.baroms.append(self.barom)
            while len(self.temps) > self.width:
                self.temps.pop(0)
            while len(self.humids) > self.width:
                self.humids.pop(0)
            while len(self.baroms) > self.width:
                self.baroms.pop(0)

    def battery(self, v, p):
        self.voltage = v
        self.percentage = p


def main():
    from lib.ups import UPS
    from time import sleep
    from lib.ahtx0 import AHT20
    from lib.mylib import CreateI2C
    from PiicoDev_MS5637 import PiicoDev_MS5637

    seconds_between_updates = 30
    graph_minutes = 30
    weather = Weather(graph_every=graph_minutes*60//seconds_between_updates)

    i2c = CreateI2C()
    ups = UPS()
    pressure = PiicoDev_MS5637(i2c)
    sensors_enabled = False
    sensor = AHT20(i2c)
    sensors_enabled = True



    while True:
        v, c, P = ups.do_reading()
        weather.battery(v, P)
        if sensors_enabled:
            weather.vals(sensor.temperature, sensor.relative_humidity, pressure.read_pressure())
        weather.update()
        sleep(seconds_between_updates)


if __name__ == '__main__':
    weather = Weather(graph_every=1)
    for i in range(weather.width):
        weather.vals(randrange(15, 32), randrange(20, 50), randrange(900, 1100))
    weather.battery(4, 90)
    weather.update()
