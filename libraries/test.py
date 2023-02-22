from pico import Pico
from screen import SSD1306_I2C

display = SSD1306_I2C(128, 32, Pico.i2c_create())
display.fill(0)
display.text("%.1f"%(500.1), 0, 0, 1, size=4)
display.show()
