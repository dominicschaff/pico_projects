from machine import I2C, Pin
from epd import EPD_2in9
from random import uniform

def CreateI2C(sda=0, scl=1):
    return I2C(0,sda=Pin(sda), scl=Pin(scl))
    

class Screen:
    def __init__(self):
        self.epd = EPD_2in9()
        self.epd.Clear(0xff)
        self.epd.fill(0xff)
    
    def clear(self):
        self.epd.Clear(0xff)
        self.epd.fill(0xff)
    
    def text(self, s, x, y):
        self.epd.text(s, x, y, 0)
    
    def text_center(self, s, x, y):
        c = len(s) * 4
        self.epd.text(s, x-c, y-4, 0)
    
    def box(self, x, y, s):
        self.epd.rect(x-s//2, y-s//2, s, s, 0)
    
    def box_fill(self, x, y, s, c=0):
        self.epd.fill_rect(x-s//2, y-s//2, s, s, c)
    
    def show(self):
        self.epd.display_Base(self.epd.buffer)
        self.epd.delay_ms(2000)
    
    def show_partial(self):
        self.epd.display_Partial(self.epd.buffer)
    
    def sleep(self):
        self.epd.sleep()
    
    def graph(self, title, values, x, y, h):
        self.text_center(title, x, y-h//2-8)
        w = len(values)
        
        self.epd.rect(x-w//2-1, y-h//2-1, w+2, h+2, 0)
        
        v_min, v_max = min(values), max(values)
        
        if v_max - v_min < 1:
            scale = h
        else:
            scale = h/(v_max - v_min)
        
        sx, sy = x-w//2-1, y+h//2-1
        py = int((values[0]-v_min)*scale)
        
        for i, v in enumerate(values):
            e = int((v-v_min)*scale)
            self.epd.line(sx+i, sy - py, sx+1+i, sy - e, 0)
            py=e

class Weather:
    def __init__(self):
        self.screen = Screen()
        self.temps = []
        self.humids = []
        self.baroms = []
        self.temp = 0
        self.humid = 0
        self.barom = 0
        self.last = 0
    
    def update(self):
        self.screen.clear()
        self.screen.box(21, 21, 42)
        self.screen.box(64, 21, 42)
        self.screen.box(107, 21, 42)
        self.screen.text_center("%.1f" % self.temp, 21, 21)
        self.screen.text_center("%.0f%%" % self.humid, 64, 21)
        self.screen.text_center("%.0f" % self.barom, 107, 21)
        
        self.screen.graph("Temperature:", self.temps, 64, 100, 50)
        self.screen.graph("Humidity:", self.humids, 64, 175, 50)
        self.screen.graph("Barometer:", self.baroms, 64, 250, 50)
        self.screen.show()
    
    def vals(self, temp, humid, barom):
        self.temp = temp
        self.humid = humid
        self.barom = barom
        self.last -= 1
        if self.last <= 1:
            self.last = 30
            self.temps.append(self.temp)
            self.humids.append(self.humid)
            self.baroms.append(self.barom)
            while len(self.temps) > 100:
                self.temps.pop(0)
            while len(self.humids) > 100:
                self.humids.pop(0)
            while len(self.baroms) > 100:
                self.baroms.pop(0)
