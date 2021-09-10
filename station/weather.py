from screen import Screen
from lcd import BLACK, WHITE
from random import randrange

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
        self.current = 0
        self.percentage = 0

    def update(self):
        self.screen.clear()
        self.screen.rect_fill(0, 0, 160, 10, BLACK)
        self.screen.text_center("%.1fV %.0f mA %2.0f%%" % (self.voltage, self.current, self.percentage), 80, 5, WHITE)

        self.screen.text_center("%.1f" % self.temp, 30, 21, BLACK)
        self.screen.text_center("%.0f%%" % self.humid, 80, 21, BLACK)
        self.screen.text_center("%.0f" % self.barom, 130, 21, BLACK)

        self.screen.rect(5, 21 - 10, 45, 20, BLACK)
        self.screen.rect(55, 21 - 10, 45, 20, BLACK)
        self.screen.rect(105, 21 - 10, 45, 20, BLACK)

        self.screen.graph("Temp:", self.temps, 30, 80, 50)
        self.screen.text_center("%.0f<%.0f" % (min(self.temps), max(self.temps)), 30, 115, BLACK)

        self.screen.graph("Humi:", self.humids, 80, 80, 50)
        self.screen.text_center("%.0f<%.0f" % (min(self.humids), max(self.humids)), 80, 115, BLACK)
        
        self.screen.graph("Baro:", self.baroms, 130, 80, 50)
        self.screen.text_center("%.1f<%.1f" % (min(self.baroms)/1000, max(self.baroms)/1000), 130, 115, BLACK)
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
            while len(self.temps) > 50:
                self.temps.pop(0)
            while len(self.humids) > 50:
                self.humids.pop(0)
            while len(self.baroms) > 50:
                self.baroms.pop(0)

    def battery(self, v, c, p):
        self.voltage = v
        self.current = c
        self.percentage = p


if __name__ == '__main__':
    weather = Weather(graph_every=1)
    for i in range(50):
        weather.vals(randrange(15, 32), randrange(20, 50), randrange(900, 1100))
    weather.battery(4, 0.1, 90)
    weather.update()

