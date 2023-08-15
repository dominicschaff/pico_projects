import board
import time
from adafruit_ds3231 import DS3231
import displayio

displayio.release_displays()

rtc = DS3231(board.I2C())
rtc.datetime = time.localtime()