from mylib import Weather, CreateI2C

import utime

import ahtx0

i2c = CreateI2C()

# 30(minutes), 60(seconds per minute), 2(refreshes twice a minute)
weather = Weather(graph_every=30*60*2)

sensor = ahtx0.AHT10(i2c)

while True:
    weather.vals(sensor.temperature, sensor.relative_humidity, 0)
    weather.update()
    utime.sleep(30)

