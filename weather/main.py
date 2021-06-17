from mylib import Weather, CreateI2C

import utime
from machine import Pin, I2C

import ahtx0

# cause a wait
led = Pin(25, Pin.OUT)
for i in range(10):
    led.toggle()
    utime.sleep(0.5)

# I2C for the Wemos D1 Mini with ESP8266
i2c = CreateI2C()
weather = Weather()

# Create the sensor object using I2C
sensor = ahtx0.AHT10(i2c)

while True:
    weather.vals(sensor.temperature, sensor.relative_humidity, 0)
    weather.update()
    utime.sleep(60)

