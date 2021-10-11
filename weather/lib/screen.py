from lcd import LCD, WHITE, BLACK, GREEN, RED, CYAN

class Screen:
    def __init__(self):
        self.lcd = LCD()
        self.lcd.fill(WHITE)
        self.lcd.show()

    def clear(self):
        self.lcd.fill(WHITE)
        self.lcd.show()

    def text(self, s, x, y, colour):
        self.lcd.text(s, x, y, colour)

    def text_center(self, s, x, y, colour):
        self.lcd.text(s, x - len(s) * 4, y-4, colour)
    
    def text_right(self, s, x, y, colour):
        self.lcd.text(s, x - len(s)*8, y-4, colour)

    def box(self, x, y, s, colour):
        self.lcd.rect(x-s//2, y-s//2, s, s, colour)

    def box_fill(self, x, y, s, c=0):
        self.lcd.fill_rect(x-s//2, y-s//2, s, s, c)

    def rect(self, xs, ys, xe, ye, c=0):
        self.lcd.rect(xs, ys, xe, ye, c)

    def rect_fill(self, xs, ys, xe, ye, c=0):
        self.lcd.fill_rect(xs, ys, xe, ye, c)

    def hline(self, y, colour):
        self.lcd.hline(0, y, self.lcd.width, colour)

    def show(self):
        self.lcd.show()

    def graph(self, title, values, x, y, h, w):
        self.lcd.rect(x-w//2-1, y-h//2-1, w+2, h+2, BLACK)
        self.text_center(title, x, y, CYAN)
        self.text_center("%.0f" % max(values), x, y - h//2 + 5, RED)
        self.text_center("%.0f" % min(values), x, y + h//2 - 4, GREEN)

        v_min, v_max = min(values), max(values)

        if v_max - v_min < 1:
            scale = h
        else:
            scale = h/(v_max - v_min)

        sx, sy = x-w//2-1, y+h//2-1
        py = int((values[0]-v_min)*scale)

        for i, v in enumerate(values):
            e = int((v-v_min)*scale)
            self.lcd.line(sx+i, sy - py, sx+1+i, sy - e, BLACK)
            py=e

