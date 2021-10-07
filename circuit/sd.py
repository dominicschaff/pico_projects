
import busio
import sdcardio
import storage
import board

class SD:
    def __init__(self, p1=board.GP10, mosi=board.GP11, miso=board.GP12, cs=board.GP15):
        self.data = p1
        self.mosi = mosi
        self.miso = miso
        self.cs = cs
    
    def mount(self):
        self.spi = busio.SPI(self.data, MOSI=self.mosi, MISO=self.miso)
        self.sd = sdcardio.SDCard(self.spi, self.cs)
        self.vfs = storage.VfsFat(self.sd)
        storage.mount(self.vfs, '/sd')
    def unmount(self):
        storage.umount(self.vfs)
        self.spi.deinit()
        self.sd.deinit()
        
