"""
Escape room animations.
"""

import time

import cv2
import numpy as np
import pygame

from draw import DRAW_RES, draw_dots, draw_text

# Global to track code across threads.
CODE = []
MAX_CODE_LEN = 4
CODE_ANS = "1234"

LAST_KEYDOWN_TIME = 0

# "SCREENSAVER", "KEY", or "UNLOCK".
STATE = "SCREENSAVER"


def keydown(key: pygame.key):
    """
    Keydown handler.
    """
    global CODE, LAST_KEYDOWN_TIME

    LAST_KEYDOWN_TIME = time.time()

    if key == pygame.K_BACKSPACE:
        if CODE:
            CODE.pop()
    else:
        rep = None
        for i in range(10):
            if key in (getattr(pygame, f"K_{i}"), getattr(pygame, f"K_KP{i}")):
                rep = str(i)
                break
        if rep is not None and len(CODE) < MAX_CODE_LEN:
            CODE.append(rep)

    print("Current code:", "".join(CODE))


def screensaver(display):
    """
    Show screensaver animation.
    """
    global STATE

    while display.run:
        time.sleep(0.5)
        dots = np.random.rand(27, 81) > 0.5
        img = draw_dots(dots)

        if STATE == "SCREENSAVER":
            display.render(img)


def show_key(display):
    """
    Show key currently typed.
    """
    global STATE

    index_to_x = lambda i: (i - 1.5) * 200 + DRAW_RES[0] / 2

    while display.run:
        time.sleep(1 / 30)

        if STATE == "KEY":
            surf = pygame.Surface(DRAW_RES)
            surf.fill((0, 0, 0))

            for i in range(len(CODE)):
                draw_text(surf, CODE[i], (int(index_to_x(i)), DRAW_RES[1] // 2 + 20))

            blink = int(time.time() * 5) % 2 == 0
            if blink:
                x = index_to_x(min(len(CODE), MAX_CODE_LEN - 1))
                y = DRAW_RES[1] - 90
                pygame.draw.rect(surf, (255, 255, 255), (int(x - 50), y - 3, 100, 6))

            # Convert to np array
            img = pygame.surfarray.array3d(surf).swapaxes(0, 1)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

            dots_border = np.full((27, 81), False, dtype=bool)
            dots_border[0] = True
            dots_border[-1] = True
            dots_border[:, 0] = True
            dots_border[:, -1] = True
            dots_mask = draw_dots(dots_border)

            dots_img = np.where(dots_mask > 0, 255, 0).astype(np.uint8)
            img = cv2.bitwise_or(img, dots_img)

            display.render(img)


def show_unlock(display):
    """
    Show unlock animation.
    """
    global STATE

    while display.run:
        time.sleep(0.5)

        if STATE == "UNLOCK":
            display.render(np.full((300, 900), 255, dtype=np.uint8))


def main(display):
    """
    Changes state based on conditions.
    """
    global CODE, STATE

    while display.run:
        time.sleep(1 / 60)

        if STATE != "UNLOCK":
            STATE = "KEY" if time.time() - LAST_KEYDOWN_TIME < 5 else "SCREENSAVER"

            if "".join(CODE) == CODE_ANS:
                STATE = "UNLOCK"

        if STATE == "SCREENSAVER":
            CODE = []
