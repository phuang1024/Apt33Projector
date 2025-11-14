"""
Make warp coords interactively.
"""

import time

import numpy as np
import pygame

from draw import draw_dots
from display import Display


def make_warp_coords(display: Display):
    # 0: top left. 1: top right. 2: bottom left. 3: bottom right
    corner = 0

    while display.run:
        time.sleep(1 / 60)

        # Select corner.
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            corner = corner & ~1
        if keys[pygame.K_d]:
            corner = corner | 1
        if keys[pygame.K_w]:
            corner = corner & ~2
        if keys[pygame.K_s]:
            corner = corner | 2

        # Adjust position.
        speed = 3
        if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
            speed *= 5
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            speed *= 0.2

        index = [0, 3, 1, 2][corner]
        if keys[pygame.K_UP]:
            display.warp[index][1] -= speed
        if keys[pygame.K_DOWN]:
            display.warp[index][1] += speed
        if keys[pygame.K_LEFT]:
            display.warp[index][0] -= speed
        if keys[pygame.K_RIGHT]:
            display.warp[index][0] += speed

        # Make sample image.
        dots = np.full((27, 81), True, dtype=bool)
        if int(time.time()) % 2 == 0:
            if corner == 0:
                dots[2:14, 2:41] = False
            elif corner == 1:
                dots[2:14, 40:-2] = False
            elif corner == 2:
                dots[13:-2, 2:41] = False
            elif corner == 3:
                dots[13:-2, 40:-2] = False

        img = draw_dots(dots)
        display.render(img)

    display.save_warp()
