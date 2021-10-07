import board
import busio
import adafruit_requests as requests
import adafruit_espatcontrol.adafruit_espatcontrol_socket as socket
from adafruit_espatcontrol import adafruit_espatcontrol

class WiFi:
    def __init__(self, ssid, password):
        RX = board.GP17
        TX = board.GP16
        uart = busio.UART(TX, RX, receiver_buffer_size=2048)
        self.esp = adafruit_espatcontrol.ESP_ATcontrol(uart, 115200, debug=False)
        requests.set_socket(socket, self.esp)
        self.requests = requests
        self._secrets = {
            "ssid": ssid,
            "password": password
        }
        self.esp.soft_reset()
    
    def connect(self):
        while not self.esp.is_connected:
            print("Connecting...")
            self.esp.connect(self._secrets)
        
    def myip(self):
        r = self.requests.get('http://whatismyip.akamai.com')
        return r.text

if __name__ == '__main__':
    wifi = WiFi("Nyx", "tsittins")
    wifi.connect()
    print(wifi.myip())