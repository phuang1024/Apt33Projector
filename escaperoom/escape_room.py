"""
Escape room animations.
"""

import pygame

# Global to track code across threads.
CODE = []


def escape_room_keydown(key: pygame.key):
    if key == pygame.K_BACKSPACE:
        if CODE:
            CODE.pop()
    else:
        for i in range(10):
            if key in (getattr(pygame, f"K_{i}"), getattr(pygame, f"K_KP{i}")):
                CODE.append(str(i))
                break

    print("Current code:", "".join(CODE))


def escape_room_main(display):
    pass
