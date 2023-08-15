
import adafruit_displayio_ssd1306
import displayio

from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font



class Screen:
    def __init__(self, i2c, width=128, height=32, address=0x3c, font="fonts/font.pcf", initial_text="0.0.0"):
        self.width = width
        self.height = height
        
        self.font = bitmap_font.load_font(font)
        self.display_bus = displayio.I2CDisplay(
            i2c,
            device_address=address
        )

        self.display = adafruit_displayio_ssd1306.SSD1306(
            self.display_bus,
            width=self.width,
            height=self.height
        )
        self.text_area = label.Label(self.font, text=initial_text)
        self.text_area.x = 0
        self.text_area.y = self.height//2
        self.display.show(self.text_area)
    
    def set_digit(self, num, tenths=False):
        if tenths:
            self.text_area.text = "%05.1f" % num
        else:
            self.text_area.text = "%05.0f" % num
