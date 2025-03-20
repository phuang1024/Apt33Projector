"""
Live adjust display parameters. Live save to file.

Keybinds:
Use ASXZ to select the four corners.
Use arrow keys to drag the selected corner.
Hold shift to move slower, and ctrl to move faster.
Use RF to increase and decrease radius, respectively.
"""

import argparse
import time

import numpy as np
import pygame

from display import Display

selection = 0


def key_handler(disp: Display, key):
    global selection

    if key == pygame.K_a:
        selection = 0
    elif key == pygame.K_s:
        selection = 1
    elif key == pygame.K_x:
        selection = 2
    elif key == pygame.K_z:
        selection = 3

    disp.params.save("disp.json")


def draw_daemon(disp: Display):
    iter = 0
    while disp.run:
        disp.board = np.ones_like(disp.board, dtype=bool)
        if selection == 0:
            index = (0, 0)
        elif selection == 1:
            index = (0, -1)
        elif selection == 2:
            index = (-1, -1)
        elif selection == 3:
            index = (-1, 0)
        else:
            raise ValueError("Invalid selection")
        disp.board[index] = iter % 2

        iter += 1
        time.sleep(0.2)


def keypress_daemon(disp: Display):
    while disp.run:
        keys = pygame.key.get_pressed()
        shift = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
        ctrl = keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]

        # Drag
        attr = ["tl", "tr", "br", "bl"][selection]
        value = getattr(disp.params, attr)
        delta = np.array([0, 0], dtype=float)
        if keys[pygame.K_UP]:
            delta[0] += -1
        if keys[pygame.K_DOWN]:
            delta[0] += 1
        if keys[pygame.K_LEFT]:
            delta[1] += -1
        if keys[pygame.K_RIGHT]:
            delta[1] += 1
        if shift:
            delta *= 0.1
        if ctrl:
            delta *= 10
        value = value + delta
        setattr(disp.params, attr, (value[0], value[1]))

        # Radius
        delta = 0
        if keys[pygame.K_r]:
            delta += 0.1
        if keys[pygame.K_f]:
            delta += -0.1
        if shift:
            delta *= 0.1
        if ctrl:
            delta *= 10
        disp.params.radius += delta

        time.sleep(0.05)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true")
    args = parser.parse_args()

    disp = Display(load_params=not args.reset)

    disp.add_daemon(draw_daemon, (disp,))
    disp.add_daemon(keypress_daemon, (disp,))
    disp.keydown_hooks.append(key_handler)

    disp.start()


if __name__ == "__main__":
    main()
