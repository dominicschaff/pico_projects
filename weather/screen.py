from epd import EPD_2in9

class Screen:
    def __init__(self):
        self.epd = EPD_2in9()
        self.epd.Clear(0xff)
        self.epd.fill(0xff)

    def clear(self):
        self.epd.Clear(0xff)
        self.epd.fill(0xff)

    def text(self, s, x, y):
        self.epd.text(s, x, y, 0)

    def text_center(self, s, x, y):
        c = len(s) * 4
        self.epd.text(s, x-c, y-4, 0)

    def box(self, x, y, s):
        self.epd.rect(x-s//2, y-s//2, s, s, 0)

    def box_fill(self, x, y, s, c=0):
        self.epd.fill_rect(x-s//2, y-s//2, s, s, c)

    def hline(self, y):
        self.epd.hline(0, y, self.epd.width, 0x00)

    def show(self):
        self.epd.display_Base(self.epd.buffer)
        self.epd.delay_ms(2000)

    def show_partial(self):
        self.epd.display_Partial(self.epd.buffer)

    def sleep(self):
        self.epd.sleep()

    def graph(self, title, values, x, y, h):
        self.text_center(title, x, y-h//2-8)
        w = len(values)

        self.epd.rect(x-w//2-1, y-h//2-1, w+2, h+2, 0)

        v_min, v_max = min(values), max(values)

        if v_max - v_min < 1:
            scale = h
        else:
            scale = h/(v_max - v_min)

        sx, sy = x-w//2-1, y+h//2-1
        py = int((values[0]-v_min)*scale)

        for i, v in enumerate(values):
            e = int((v-v_min)*scale)
            self.epd.line(sx+i, sy - py, sx+1+i, sy - e, 0)
            py=e

