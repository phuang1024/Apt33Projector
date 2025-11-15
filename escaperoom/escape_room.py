"""
Escape room animations.
"""

import time
from threading import Thread

import cv2
import numpy as np
import pygame

from draw import DRAW_RES, draw_dots, draw_text
from screensaver import screensaver_main

# Global to track code across threads.
CODE = []
MAX_CODE_LEN = 4
CODE_ANS = "2038"

LAST_KEYDOWN_TIME = 0
UNLOCK_TIME = 0

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

    board = np.full((27, 81), False, dtype=bool)
    anim_thread = Thread(target=screensaver_main, args=(display, board))
    anim_thread.start()

    while display.run:
        time.sleep(1 / 60)

        if STATE == "SCREENSAVER":
            img = draw_dots(board)
            display.render(img)

    anim_thread.join()


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
                y = DRAW_RES[1] - 60
                pygame.draw.rect(surf, (255, 255, 255), (int(x - 50), y - 4, 100, 8))

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

    video = cv2.VideoCapture("answer.mp4")

    while display.run:
        if STATE == "UNLOCK":
            for _ in range(2):
                ret, frame = video.read()
            if not ret:
                time.sleep(3)
                video.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            display.render(gray)

        else:
            video.set(cv2.CAP_PROP_POS_FRAMES, 0)

        time.sleep(0.07 if STATE == "UNLOCK" else 0.5)


def main(display):
    """
    Changes state based on conditions.
    """
    global CODE, STATE, UNLOCK_TIME

    while display.run:
        time.sleep(1 / 60)

        if STATE != "UNLOCK":
            STATE = "KEY" if time.time() - LAST_KEYDOWN_TIME < 5 else "SCREENSAVER"

            if "".join(CODE) == CODE_ANS:
                STATE = "UNLOCK"
                UNLOCK_TIME = time.time()

        else:
            if time.time() - UNLOCK_TIME > 60:
                STATE = "SCREENSAVER"

        if STATE == "SCREENSAVER":
            CODE = []
