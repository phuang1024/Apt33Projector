"""
Live adjust display parameters. Live save to file.

Keybinds:
Pressing corresponding key increases value.
Ctrl pressing key decreases value.
Shift pressing changes in small increments.
"""

import numpy as np
import pygame

from display import Display
from random_bw import random_bw

KEY_ATTRS = {
    pygame.K_s: "radius",
    pygame.K_r: "rotation",
    pygame.K_x: "x_ival",
    pygame.K_y: "y_ival",
    pygame.K_UP: "y_offset",
    pygame.K_RIGHT: "x_offset",
    pygame.K_p: "x_persp",
    pygame.K_o: "y_persp",
    pygame.K_z: "x_stretch",
}


def key_handler(disp: Display, key):
    key_pressed = pygame.key.get_pressed()
    shift = key_pressed[pygame.K_LSHIFT] or key_pressed[pygame.K_RSHIFT]
    ctrl = key_pressed[pygame.K_LCTRL] or key_pressed[pygame.K_RCTRL]

    if key in KEY_ATTRS:
        attr = KEY_ATTRS[key]
        value = getattr(disp.params, attr)
        if attr in ("x_persp", "y_persp", "x_offset", "y_offset"):
            delta = 10
        else:
            delta = 0.1
        if shift:
            delta *= 0.1
        if ctrl:
            delta *= -1
        new_value = value + delta
        setattr(disp.params, attr, new_value)

        print(f"{attr} = {new_value}")

        # Save to file
        disp.params.save("disp.json")


def main():
    disp = Display()

    disp.board = np.ones_like(disp.board, dtype=bool)
    #disp.add_daemon(random_bw, (disp,))
    disp.keydown_hooks.append(key_handler)

    disp.start()


if __name__ == "__main__":
    main()
