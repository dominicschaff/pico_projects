# Basic Speedometer

This is an intial basic setup for a speedometer. It is designed for a motorbike.

This is still currently very much work in progress, and some of the code is for
testing purposes and not yet suitable for use.


## Components used

* Main board:
    * [Raspberry Pico](https://www.robotics.org.za/PI-PICO)
    * For a smaller design I also used: [Wave Pi Pico](https://www.robotics.org.za/W20187)
* Display:
    * [Small OLED](https://www.robotics.org.za/OLED-91-WHI?search=oled)
* Stepper Motors:
    * [Control Board](https://www.robotics.org.za/3133)
    * [Stepper Motor](https://www.robotics.org.za/20BYGH306)
* Sensors:
    * [Magnetic Sensor](https://www.robotics.org.za/A3144)
    * [Light Sensor](https://www.robotics.org.za/LDR-10K) + 10k resistor


## Connection Setup

* Screen and Stepper control board using i2c on GP0 and GP1
* Magnetic Sensor on GP2
* LDR on A0 or GP26


## Libraries used:

* [Adafruit Framebuf](https://github.com/adafruit/Adafruit_CircuitPython_framebuf)
* [Adafruit SSD1306](https://github.com/adafruit/Adafruit_CircuitPython_SSD1306)
* Stepper control software is based on [Pololu Documentation](https://www.pololu.com/docs/0J71/12.9)
