from maker import Maker
import board
import time
from sd import SD
from wifi import WiFi
from json import dumps

m = Maker()

sd = SD()
wifi = WiFi()
sd.mount()

LEDS = [m.led(board.GP2), m.led(board.GP3), m.led(board.GP4)]
            
while True:

    if m.b1():
        LEDS[0].value = True
        aps = [{
            'ssid': ap[1],
            'bssid': ap[3],
            'strength': ap[2],
            'channel': ap[4],
            'other': [ap[0], ap[5], ap[6]]
            } for ap in wifi.scan()]
        
        sd.write("wifi.json", dumps(aps), append=True)
        LEDS[0].value = False

    elif m.b2():
        LEDS[1].value = True
        m.mouse.press(1)
        while not m.b2():
            time.sleep(0.05)
        m.mouse.release(1)
        #sd.write("temp.txt", dumps({"temp": m.temp()}), append=True)
        LEDS[1].value = False

    elif m.b3():
        LEDS[2].value = True
        while not m.b3():
            m.mouse_left()
            time.sleep(0.05)
        LEDS[2].value = False
    time.sleep(0.1)
