# PiicoDev MS5637 minimal example code
# This program temperature and pressure data from the PiicoDev MS5637 pressure sensor
# and displays the result

from PiicoDev_MS5637 import PiicoDev_MS5637
from PiicoDev_Unified import sleep_ms
from lib.ahtx0 import AHT20
from lib.mylib import CreateI2C

i2c = CreateI2C()
print(i2c.scan())
pressure = PiicoDev_MS5637(i2c)
sensor = AHT20(i2c)

while True:
    press_hPa = pressure.read_pressure()
    altitude_m = pressure.read_altitude()

    # Print Pressure
    print(str(press_hPa) + " hPa")
    
    # Print Altitude (metres)
#     print(str(altitude_m) + " m")
    sleep_ms(100)
    