import argparse
import random
import time
from threading import Thread

import numpy as np

from display import Display
from draw import draw_dots
from make_warp import make_warp_coords
from escape_room import escape_room_main, escape_room_keydown


def test_random(display: Display):
    while display.run:
        dots = np.random.rand(27, 81) > 0.5
        img = draw_dots(dots)
        display.render(img)

        time.sleep(0.5)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--warp", action="store_true", help="Enter interactive warp mode.")
    args = parser.parse_args()

    display = Display()

    if args.warp:
        threads = [
            Thread(target=make_warp_coords, args=(display,)),
        ]

    else:
        display.add_keydown_callback(escape_room_keydown)
        threads = [
            Thread(target=escape_room_main, args=(display,)),
        ]

    for thread in threads:
        thread.start()
    display.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
