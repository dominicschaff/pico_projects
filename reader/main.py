from epd_large import EPD
from text_function import split
import utime

def show_page(epd, page, page_number, total, title):
    epd.image4Gray.fill(epd.white)
    epd.image4Gray.fill_rect(0, 0, 400, 15, epd.black)
    epd.image4Gray.text("[%d/%d] %s" % (page_number, total, title[:35]), 5, 5, epd.white)
    for i, line in enumerate(page):
        epd.image4Gray.text(line, 5, 10*(i + 2), epd.black)
    epd.EPD_4GrayDisplay(epd.buffer_4Gray)

f = open('data.txt')
text = f.read()
f.close()

pages = split(text)
total = len(pages)

title = pages[0][0]

epd = EPD()
while True:
    for i, page in enumerate(pages):
        show_page(epd, page, i+1, total, title)
        utime.sleep(30)

