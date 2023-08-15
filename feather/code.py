import board
import displayio
import terminalio
import adafruit_displayio_sh1107
import neopixel
import time
from adafruit_dps310.basic import DPS310
from adafruit_ahtx0 import AHTx0
from adafruit_display_text.label import Label
import digitalio
from adafruit_ds3231 import DS3231
from adafruit_msa3xx import MSA311
from adafruit_vcnl4040 import VCNL4040
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.line import Line
import adafruit_imageload
import busio
from random import randint

displayio.release_displays()

ADDRESS_AHT20 = '0x38'
ADDRESS_OLED = '0x3c'
ADDRESS_MSA = '0x62'
ADDRESS_RTS = '0x68'
ADDRESS_DPS = '0x77'
ADDRESS_VCNL = '0x60'
        
DAY_NAMES = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")

def map_range(s, a1, a2, b1, b2):
    return  b1 + ((s - a1) * (b2 - b1) / (a2 - a1))


class Feather:
    def __init__(self):
        self.i2c = busio.I2C( board.SCL, board.SDA, frequency=400_000)
        self.up = self.button(board.D9)
        self.select = self.button(board.D6)
        self.down = self.button(board.D5)
    
    def setup_screen(self):
        display_bus = displayio.I2CDisplay(self.i2c, device_address=0x3C)
        self.WIDTH = 128
        self.HEIGHT = 64
        
        self.display = adafruit_displayio_sh1107.SH1107(display_bus, width=self.WIDTH, height=self.HEIGHT, auto_refresh=False)
        
        self.neo = neopixel.NeoPixel(board.NEOPIXEL, 1)
        self.neo.brightness = 0.3
        
        self.main_group = displayio.Group()
        
        self.menu_text = self._create_label(self.main_group, 0, 60, "TITLE")
    
        self.use_group = displayio.Group()
        self.main_group.append(self.use_group)

        self.display.show(self.main_group)
    
    def refresh(self, sleep=0.0):
        self.display.refresh()
        time.sleep(sleep)
        
    def menu(self, options=None):
        while not self.down.value or not self.up.value or not self.select.value:
            time.sleep(0.1)
        if options is None:
            options = [
                {"name": "Desk", "function": self.clock},
                {"name": "Weather", "function": self.weather},
                {"name": "Screensaver", "function": self.screensaver},
                {"name": "Accelerometer", "function": self.balance},
                {"name": "Proximity", "function": self.proximity},
                {"name": "Scanner", "function": self.scanner},
            ]
        rtc = DS3231(self.i2c)
        clock = self._create_label(self.use_group, 0, 16, "", centre_x=True, scale=2)
        selected = 0
        self.menu_text.text = ">" + options[selected]['name']
        count = len(options) - 1
        ti = 0
        while self.select.value:
            if self._selected_and_wait(self.down):
                selected = min(selected + 1, count)
                self.menu_text.text = ">" + options[selected]['name']
            if self._selected_and_wait(self.up):
                selected = max(selected - 1, 0)
                self.menu_text.text = ">" + options[selected]['name']
            if ti != time.time():
                ti = time.time()
                t = rtc.datetime
                clock.text = "%02d:%02d:%02d" % (t.tm_hour, t.tm_min, t.tm_sec)
            self.refresh()
        
        try:
            self._clear_main()
            options[selected]['function']()
            self._selected_and_wait(self.down)
            self._clear_main()
        except ValueError as ve:
            self.show_error(ve)
    
    def _selected_and_wait(self, button):
        if button.value == False:
            while button.value == False:
                pass
            return True
        return False
    
    def _clear_main(self):
        for i in range(len(self.use_group)):
            del self.use_group[0]
        self.neo.fill((0,0,0))
    
    def show_error(self, err):
        self.menu_text.text = "Missing: " + str(err)
        while self.down.value:
            self.refresh()
    
    def weather(self):
        devices = self.scan_i2c()
        if ADDRESS_AHT20 not in devices or ADDRESS_DPS not in devices:
            raise ValueError('AHT20 and DPS310')
        ahtx = AHTx0(self.i2c)
        dps310 = DPS310(self.i2c)
        
        temp = self._create_label(self.use_group, 64, 8, "Temp", centre_point=True)
        humid = self._create_label(self.use_group, 64, 24, "Humid", centre_point=True)
        height = self._create_label(self.use_group, 64, 40, "Height", centre_point=True)
        
        while self.down.value:
            temp.text = "%.1f C" % ahtx.temperature
            humid.text = "%.1f %%" % ahtx.relative_humidity
            height.text = "%.1f bar" % dps310.pressure
            self.neo.fill(self.wheel(255-int(ahtx.temperature * 5)))
            self.refresh(0.5)
        
        self.menu_text.text = "Good bye"
    
    def clock(self):
        devices = self.scan_i2c()
        if ADDRESS_RTS not in devices:
            raise ValueError('RTC|DS3231')
        
        enable_weather = ADDRESS_AHT20 in devices
        
        rtc = DS3231(self.i2c)
        
        clock = self._create_label(self.use_group, 48, 16, "00:00", scale=3, centre_point=True)
        seconds = self._create_label(self.use_group, 116, 16, "00", scale=2, centre_point=True)

        if enable_weather:
            weather = self._create_label(self.use_group, self.WIDTH // 2, 42, "", centre_point=True)
            ahtx = AHTx0(self.i2c)

        ti = 0
        while self.down.value:
            if ti != time.time():
                ti = time.time()
                t = rtc.datetime
                clock.text = "%02d:%02d" % (t.tm_hour, t.tm_min)
                seconds.text = "%02d" % (t.tm_sec)
                self.menu_text.text = "%s %04d/%02d/%02d" % (
                    DAY_NAMES[int(t.tm_wday)], t.tm_year, t.tm_mon, t.tm_mday
                )
                if enable_weather:
                    weather.text = "%.0f C %.0f %%" % (ahtx.temperature, ahtx.relative_humidity)
            self.refresh()
        self.menu_text.text = "Good bye"
    
    def balance(self):
        devices = self.scan_i2c()
        if ADDRESS_MSA not in devices:
            raise ValueError('Accelerometer')
        
        msa = MSA311(self.i2c)
        circle = Circle(64, 32, 1, fill=0xFFFFFF)
        
        line_y = Line(64, 24, 64, 40, 0xFFFFFF)
        line_x = Line(56, 32, 72, 32, 0xFFFFFF)
        
        self.use_group.append(circle)
        self.use_group.append(line_y)
        self.use_group.append(line_x)
        while self.down.value:
            x,y,z = msa.acceleration
            circle.x = int(map_range(y, -10, 10, 0, 128))
            circle.y = int(map_range(-x, -10, 10, 0, 64))
            self.menu_text.text = "%6.3f %6.3f %6.3f" % (x,y,z)
            self.refresh()
        self.menu_text.text = "Good bye"
    
    def proximity(self):
        devices = self.scan_i2c()
        if ADDRESS_VCNL not in devices:
            raise ValueError('Proximity')
        
        vcnl = VCNL4040(self.i2c)
        proximity = self._create_label(self.use_group, 32, 8, "", scale=2, centre_point=True)
        lux = self._create_label(self.use_group, 32, 32, "", scale=2, centre_point=True)
        while self.down.value:
            proximity.text = "%d" % vcnl.proximity
            lux.text = "%d" % vcnl.lux
            self.refresh()
        self.menu_text.text = "Good bye"

    def scanner(self):
        addresses = self.scan_i2c()
        lookup = {
            ADDRESS_AHT20: "AHT20",
            ADDRESS_OLED: "OLED",
            ADDRESS_MSA: "MSA",
            ADDRESS_RTS: "RTS",
            ADDRESS_DPS: "DPS",
            ADDRESS_VCNL: "VCNL"
        }
        
        lines = [[]]
        for a in addresses:
            if len(lines[-1]) < 3:
                lines[-1].append(lookup.get(a, a))
            else:
                lines.append([lookup.get(a, a)])
        
        output = "\n".join([", ".join(line) for line in lines])
        self._create_label(self.use_group, 8, 8, output)
        self.refresh()

        while self.down.value:
            pass
        self.menu_text.text = "Good bye"
    
    def screensaver(self):
        rtc = DS3231(self.i2c)
        
        drops = [
            Circle(
                x0=randint(0, self.WIDTH),
                y0=randint(0, self.HEIGHT),
                r=randint(1, 15),
                outline=0xFFFFFF,
                stroke=1
            ) for i in range(12)
        ]
        for d in drops:
            self.use_group.append(d)
        
        t = 0
        pos = 0
        while self.down.value:
            for d in drops:
                d.x = min(max(10, d.x + randint(-2, 2)), self.WIDTH)
                d.y = min(max(10, d.y + randint(-2, 2)), self.HEIGHT)
            if time.time() != t:
                t = time.time()
                d = rtc.datetime
                self.menu_text.text = "%02d:%02d:%02d" % (d.tm_hour, d.tm_min, d.tm_sec)
            self.neo.fill(self.wheel(pos))
            pos = (pos + 1) % 256
            self.refresh()

    def _create_label(self, group, x, y, text="T", scale=1, centre_x=False, centre_point=False):
        label = Label(terminalio.FONT, text=text, scale=scale, x=x, y=y)
        if centre_x:
            label.anchor_point = (0.5, 0.5)
            label.anchored_position = (self.WIDTH / 2, y)
        if centre_point:
            label.anchor_point = (0.5, 0.5)
            label.anchored_position = (x, y)
        group.append(label)
        return label
    
    def wheel(self, pos):
        # Input a value 0 to 255 to get a color value.
        # The colours are a transition r - g - b - back to r.
        if pos < 0 or pos > 255:
            return (0, 0, 0)
        if pos < 85:
            return (255 - pos * 3, pos * 3, 0)
        if pos < 170:
            pos -= 85
            return (0, 255 - pos * 3, pos * 3)
        pos -= 170
        return (pos * 3, 0, 255 - pos * 3)

    def button(self, pin, pull=digitalio.Pull.UP):
        b = digitalio.DigitalInOut(pin)
        b.switch_to_input(pull=pull)
        return b
    
    def scan_i2c(self):
        while not self.i2c.try_lock():
            pass
        addresses = [hex(device_address) for device_address in self.i2c.scan()]
        self.i2c.unlock()
        return addresses

if __name__ == '__main__':
    feather = Feather()
    feather.setup_screen()
    while True:
        feather.menu()