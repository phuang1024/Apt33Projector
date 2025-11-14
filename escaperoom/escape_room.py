"""
Escape room animations.
"""

import time

import numpy as np
import pygame

from draw import draw_dots

# Global to track code across threads.
CODE = []
LAST_KEYDOWN_TIME = 0
SHOW_KEY = False


def keydown(key: pygame.key):
    global CODE, LAST_KEYDOWN_TIME

    LAST_KEYDOWN_TIME = time.time()

    if key == pygame.K_BACKSPACE:
        if CODE:
            CODE.pop()
    else:
        for i in range(10):
            if key in (getattr(pygame, f"K_{i}"), getattr(pygame, f"K_KP{i}")):
                CODE.append(str(i))
                break

    print("Current code:", "".join(CODE))


def screensaver(display):
    global SHOW_KEY

    while display.run:
        time.sleep(0.5)
        dots = np.random.rand(27, 81) > 0.5
        img = draw_dots(dots)

        if not SHOW_KEY:
            display.render(img)


def main(display):
    global SHOW_KEY

    while display.run:
        time.sleep(1 / 60)

        SHOW_KEY = time.time() - LAST_KEYDOWN_TIME < 5
