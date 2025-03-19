"""
Interactively make pixel art.
"""

import os
import time

import numpy as np
import pygame

from display import Display

cursor = [0, 0]
if os.path.isfile("board.npy"):
    board = np.load("board.npy")
    assert board.shape == (27, 81)
    assert board.dtype == bool
else:
    board = np.zeros((27, 81), dtype=bool)


def key_handler(disp: Display, key):
    if key == pygame.K_RETURN:
        board[cursor[1], cursor[0]] = not board[cursor[1], cursor[0]]
    elif key == pygame.K_UP:
        cursor[1] -= 1
    elif key == pygame.K_DOWN:
        cursor[1] += 1
    elif key == pygame.K_LEFT:
        cursor[0] -= 1
    elif key == pygame.K_RIGHT:
        cursor[0] += 1
    cursor[0] = cursor[0] % board.shape[1]
    cursor[1] = cursor[1] % board.shape[0]

    disp.save_board("board.npy")


def draw_daemon(disp: Display):
    i = 0
    while disp.run:
        time.sleep(0.2)
        disp.board[:] = board
        disp.board[cursor[1], cursor[0]] = i % 2
        i += 1


def main():
    disp = Display()
    disp.keydown_hooks.append(key_handler)
    disp.add_daemon(draw_daemon, (disp,))
    disp.start()


if __name__ == "__main__":
    main()
