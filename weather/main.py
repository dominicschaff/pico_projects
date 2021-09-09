from mylib import CreateI2C
from weather import Weather

import utime

import ahtx0

i2c = CreateI2C()

# 30(minutes), 2(refreshes twice a minute)
weather = Weather(graph_every=30*2)

sensor = ahtx0.AHT10(i2c)

while True:
    weather.vals(sensor.temperature, sensor.relative_humidity)
    weather.update()
    utime.sleep(30)


