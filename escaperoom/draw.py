"""
Utilities for drawing.
"""

import cv2
import numpy as np

DRAW_RES = (900, 300)


def blank_img():
    return np.zeros(DRAW_RES[::-1], dtype=np.uint8)


def draw_dots(dots, radius=4):
    """
    dots: ndarray bool, shape (27, 81)
    """
    img = blank_img()

    for y in range(dots.shape[0]):
        for x in range(dots.shape[1]):
            if dots[y, x]:
                px_x = np.interp(x, [-1, dots.shape[1]], [0, DRAW_RES[0]])
                grid_y = y + (0.5 if x % 2 == 0 else 0)
                px_y = np.interp(grid_y, [-1, dots.shape[0]], [0, DRAW_RES[1]])

                cv2.circle(img, (int(px_x), int(px_y)), radius, 255, -1, cv2.LINE_AA)

    return img
