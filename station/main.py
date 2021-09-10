from ups import UPS
from time import sleep
from ahtx0 import AHT10
from mylib import CreateI2C
from weather import Weather

i2c = CreateI2C()
ups = UPS()
sensor = AHT10(i2c)

seconds_between_updates = 5

weather = Weather(graph_every=30*60//seconds_between_updates)

while True:
    v, c, P = ups.do_reading()
    weather.battery(v, c, P)
    weather.vals(sensor.temperature, sensor.relative_humidity, 0)
    weather.update()
    sleep(seconds_between_updates)
