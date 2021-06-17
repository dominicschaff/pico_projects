from screen import Screen

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
        self.full_refresh = True

    def update(self):
        if self.full_refresh:
            self.screen.clear()
        else:
            self.screen.box_fill(21, 21, 40, 1)
            self.screen.box_fill(64, 21, 40, 1)
            self.screen.box_fill(107, 21, 40, 1)

        self.screen.text_center("%.1f" % self.temp, 21, 21)
        self.screen.text_center("%.0f%%" % self.humid, 64, 21)
        self.screen.text_center("%.0f" % self.barom, 107, 21)

        if self.full_refresh:
            self.screen.box(21, 21, 42)
            self.screen.box(64, 21, 42)
            self.screen.box(107, 21, 42)
            self.screen.graph("Temperature:", self.temps, 64, 100, 50)
            self.screen.graph("Humidity:", self.humids, 64, 175, 50)
            self.screen.graph("Barometer:", self.baroms, 64, 250, 50)
            self.screen.show()
        else:
            self.screen.show_partial()
        self.full_refresh = False

    def vals(self, temp, humid, barom):
        print("Set: temp:%.1f | humid:%.1f | barom:%.1f" % (temp, humid, barom))
        self.temp = temp
        self.humid = humid
        self.barom = barom
        self.last -= 1
        if self.last <= 1:
            self.full_refresh = True
            self.last = self.graph_every
            self.temps.append(self.temp)
            self.humids.append(self.humid)
            self.baroms.append(self.barom)
            while len(self.temps) > 120:
                self.temps.pop(0)
            while len(self.humids) > 120:
                self.humids.pop(0)
            while len(self.baroms) > 120:
                self.baroms.pop(0)
