def main():
    from lib.mylib import Leds, Colours, Button
    from time import sleep

    leds = Leds(leds=16, inverted=True)

    scheme = Colours.random_scheme()

    def mode_up(pin):
        global scheme
        scheme = Colours.random_scheme()

    Button(15).interupt(mode_up)

    while True:
        leds.randoms(scheme, 0.5)
        leds.show()
        sleep(0.1)

if __name__ == '__main__':
    main()