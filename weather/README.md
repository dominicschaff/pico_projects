# Weather Machine

This is a basic little weather machine that I am making.

## Hardware

* Raspberry Pico <https://www.robotics.org.za/PI-PICO>
* Waveshare 2.13" Pico e-ink display <https://www.robotics.org.za/W19406>
* Adafruit AHT20 Sensor <https://www.robotics.org.za/AF4566>
* Adafruit DPS310 Sensor <https://www.robotics.org.za/AF4494>
* Adafruit VCNL4040 Sensor <https://www.robotics.org.za/AF4161>

## Libraries

* AHT20 Library: <https://github.com/targetblank/micropython_ahtx0>
* Waveshare Library: <https://github.com/waveshare/Pico_ePaper_Code/blob/main/python/Pico_ePaper-2.13.py>
* Requires OS: <https://github.com/waveshare/Pico_ePaper_Code/blob/main/python/rp2-pico-20210418-v1.15.uf2>

## Features

`*` means future plans

* Current temperature, relative humidty, and barometric reading`*`. (Accurate to the last minute)
* Graphs over the last about 2 days. (New point every 30 minutes)
  * Temperate
  * Humidity
  * `*` Barometric Pressure
* `*` Barometric Pressure - when I convert the circuit python code, or find a micropython version
