from screen import Screen

class Weather:
    def __init__(self, graph_every=10):
        self.screen = Screen()
        self.temps = []
        self.humids = []
        self.temp = 0
        self.humid = 0
        self.last = 0
        self.graph_every = graph_every

    def update(self):
        self.screen.clear()

        self.screen.text_center("%.1f" % self.temp, 32, 21)
        self.screen.text_center("%.0f%%" % self.humid, 64, 21)

        self.screen.box(32, 21, 21)
        self.screen.box(64, 21, 21)

        self.screen.graph("Temperature:", self.temps, 64, 100, 50)
        self.screen.text_center("%.1f<%.1f" % (min(self.temps), max(self.temps)), 64, 133)
        self.screen.hline(138)

        self.screen.graph("Humidity:", self.humids, 64, 180, 50)
        self.screen.text_center("%.1f<%.1f" % (min(self.humids), max(self.humids)), 64, 213)
        self.screen.hline(218)

    def vals(self, temp, humid):
        print("Set: temp:%.1f | humid:%.1f" % (temp, humid))
        self.temp = temp
        self.humid = humid
        self.last -= 1
        if self.last <= 1:
            self.last = self.graph_every
            self.temps.append(self.temp)
            self.humids.append(self.humid)
            while len(self.temps) > 120:
                self.temps.pop(0)
            while len(self.humids) > 120:
                self.humids.pop(0)


if __name__ == '__main__':
    weather = Weather(graph_every=30*2)
    weather.vals(1, 2)
    weather.update()
