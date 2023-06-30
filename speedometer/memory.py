from pico import Pico
import displayio
import board
import digitalio
import struct
import time
from adafruit_bus_device.i2c_device import (
    I2CDevice as i2cdev,
)


class Memory:
    def __init__(self, i2c, wp_pin):
        self._i2c = i2cdev(i2c, 0x50)
        self.wp = digitalio.DigitalInOut(wp_pin)
        self.wp.switch_to_output()
        self.wp.value = False
        self.last_state=[]
    
    def __getitem__(self, address):
        result = bytearray(1)
        with self._i2c as i2c:
            i2c.write_then_readinto(bytes([address]), result)
        return result[0]
    
    def __setitem__(self, address, value):
        with self._i2c as i2c:
            i2c.write(bytes([address, value]))
        time.sleep(0.005)
    
    def write_distances(self, total, trip):
        values = [i for i in struct.pack('ff', total, trip)]
        if values == self.last_state:
            return
        self.last_state = values
        with self._i2c as i2c:
            send = bytearray(1 + len(values))
            send[0] = 0
            for i in range(len(values)):
                send[i+1] = values[i]
            print([s for s in send])
            i2c.write(send)
#         time.sleep(0.005)
    
    def read_distances(self):
        return struct.unpack('ff', bytes([self[i] for i in range(8)]))
        
    
    def size(self):
        return len(self.eeprom)


if __name__ == '__main__':
    displayio.release_displays()
    i2c = Pico.i2c_create()

    memory = Memory(i2c, board.GP3)
    memory.write_distances(1.29, 5.6)
    # for i in range(100):
    #     memory[i] = i*2

    print("READ:")
    total, trip = memory.read_distances()
    print(total, trip)
    # print(memory.read(0, count=5))
    # for i in range(100):
    #     print(i, memory[i])

