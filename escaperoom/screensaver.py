"""
Screensaver animations.
"""

import random
import time

import numpy as np


# Helper functions
def get_coords(board):
    """Get a list of (x, y) coordinates that are True."""
    y, x = np.where(board)
    coords = np.stack((x, y), axis=0).swapaxes(0, 1)
    return coords


def blank_board():
    """Generate a blank board."""
    return np.zeros((27, 81), dtype=bool)


def sequential_fill(board, coords, value):
    """Fill sequentially from given (x, y) coords."""
    for x, y in coords:
        board[y, x] = value
        time.sleep(0.001)


# Animations that fill all squares.
def random_fill(board, value):
    """Fill all coords with value in a random order."""
    coords = list(get_coords(np.logical_not(blank_board())))
    random.shuffle(coords)
    sequential_fill(board, coords, value)


def left_to_right_fill(board, value):
    """Fill all coords with value from left to right."""
    y, x = np.meshgrid(range(board.shape[0]), range(board.shape[1]), indexing="xy")
    coords = np.stack((x.flatten(), y.flatten()), axis=1)
    sequential_fill(board, coords, value)


def circle_fill(board, value):
    """Fill squares with increasing radius."""
    r = 0
    while r < 50:
        r += 0.5
        for x in range(81):
            for y in range(27):
                if ((x - 40) ** 2 + (y - 13) ** 2) ** 0.5 <= r:
                    board[y, x] = value
        time.sleep(0.03)


# Animations that create patterns.
def matrix(board, mask):
    density = random.uniform(0.05, 0.1)
    iters = random.randint(150, 250)

    streaks = np.zeros((81,), dtype=int)
    matrix_board = blank_board()

    for i in range(iters):
        if i >= iters - 50:
            density = 1

        matrix_board = np.roll(matrix_board, 1, axis=0)
        matrix_board[0, :] = False

        for x in range(81):
            if random.random() <= density:
                streaks[x] = random.randint(3, 7)
            if streaks[x] > 0:
                matrix_board[0, x] = True
        streaks -= 1

        board[:] = np.logical_and(matrix_board, mask)

        time.sleep(0.05)


def screensaver_main(display, board):
    """
    board: ndarray shape (27, 81), dtype bool
        Shared object to indicate which dots are lit.
    """
    while display.run:
        matrix(board, np.full((27, 81), True, dtype=bool))
        time.sleep(2)

        erase_func = random.choice((
            random_fill,
            left_to_right_fill,
            circle_fill,
        ))
        erase_func(board, False)
        board[:] = False
        time.sleep(2)
