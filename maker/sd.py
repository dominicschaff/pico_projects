import busio
import sdcardio
import storage
import board
import os

class SD:
    def __init__(self, p1=board.GP10, mosi=board.GP11, miso=board.GP12, cs=board.GP15):
        self.data = p1
        self.mosi = mosi
        self.miso = miso
        self.cs = cs
        self._dir = "/sd"
    
    def mount(self):
        self.spi = busio.SPI(self.data, MOSI=self.mosi, MISO=self.miso)
        self.sd = sdcardio.SDCard(self.spi, self.cs)
        self.vfs = storage.VfsFat(self.sd)
        storage.mount(self.vfs, '/sd')
    def unmount(self):
        storage.umount(self.vfs)
        self.spi.deinit()
        self.sd.deinit()
    
    def cd(self, directory=None):
        if directory is not None:
            self._dir = directory
    
    def ls(self, directory=None):
        self.cd(directory)
        return [self.file_info(self._dir, file) for file in os.listdir(self._dir)]
    
    def file_info(self, path, file):
        stats = os.stat(path + "/" + file)
        filesize = stats[6]
        isdir = stats[0] & 0x4000
        if filesize < 1000:
            sizestr = str(filesize) + " by"
        elif filesize < 1000000:
            sizestr = "%0.1f KB" % (filesize / 1000)
        else:
            sizestr = "%0.1f MB" % (filesize / 1000000)
        
        return {
            "path": path,
            "name": file,
            "isdir": isdir,
            "size": filesize,
            "sizeString": sizestr,
        }
    
    def write(self, file, content, append=False):
        with open(f"{self._dir}/{file}", "a" if append else "w") as f:
            f.write(content)
            f.write("\n")
    def read(self, file):
        with open(f"{self._dir}/{file}", "r") as f:
            return f.read()
    
    def delete(self, file):
        os.remove(f"{self._dir}/{file}")
