from lib.pico import Pico
from lib.neo import Neo, WHITE, CYAN, BLACK
import board
import displayio
import time

from adafruit_displayio_sh1106 import SH1106
from adafruit_display_text.label import Label
from adafruit_bitmap_font import bitmap_font
from sound import Audio, JINGLE_BELLS, MARIO, HANUKKAH
from lib.ahtx0 import AHTx0
from lib.dps310 import DPS310


class Mine:
    def __init__(self):
        displayio.release_displays()
        self.i2c = Pico.i2c_create()
        self.neo = Neo(board.GP16, brightness=0.1, count=1)
    
    def setup(self):
        self.font = bitmap_font.load_font("fonts/UbuntuMono-Regular-16.pcf")
        self.display_bus = displayio.I2CDisplay(
            self.i2c,
            device_address=0x3c
        )
        self.display = SH1106(
            self.display_bus,
            width=128,
            height=64
        )
        self.ahtx = AHTx0(self.i2c)
        self.dps310 = DPS310(self.i2c)
        
        self.text_group = displayio.Group()
        
        self.temp = self._create_label(16, 8, "Temp")
        self.humid = self._create_label(16, 24, "Humid")
        self.temp2 = self._create_label(16, 40, "Temp2")
        self.height = self._create_label(16, 56, "Height")
        
        self.display.show(self.text_group)
    
    def _create_label(self, x, y, text="T"):
        label = Label(self.font, text=text)
        label.x, label.y = x, y
        self.text_group.append(label)
        return label
    
    def noise(self):
        audio = Audio(left=board.GP8)
        audio.buzzer_init()
        audio.play_song(HANUKKAH)
        audio.buzzer.deinit()
    
    def update(self):
        self.temp.text = "%6.1f C" % self.ahtx.temperature
        self.humid.text = "%6.1f %%" % self.ahtx.relative_humidity
        self.temp2.text = "%6.1f C" % self.dps310.temperature
        self.height.text = "%6.1f bar" % self.dps310.pressure
        self.neo.fill(self.neo.wheel(255-int(self.ahtx.temperature * 5)))
        


def main():
    mine = Mine()
    mine.setup()
    
    while True:
        mine.update()
        time.sleep(0.2)
if __name__ == '__main__':
    main()