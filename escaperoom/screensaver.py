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
def random_fill(board, value=False):
    """Fill all coords with value in a random order."""
    coords = list(get_coords(np.logical_not(blank_board())))
    random.shuffle(coords)
    sequential_fill(board, coords, value)


def left_to_right_fill(board, value=False):
    """Fill all coords with value from left to right."""
    y, x = np.meshgrid(range(board.shape[0]), range(board.shape[1]), indexing="xy")
    coords = np.stack((x.flatten(), y.flatten()), axis=1)
    sequential_fill(board, coords, value)


def circle_fill(board, value=False):
    """Fill squares with increasing radius."""
    r = 0
    while r < 50:
        r += 0.5
        for x in range(81):
            for y in range(27):
                if ((x - 40) ** 2 + (y - 13) ** 2) ** 0.5 <= r:
                    board[y, x] = value

        time.sleep(0.03)


def radial_fill(board, value=False):
    """Fill squares with increasing angle."""
    streaks = random.randint(1, 5)
    angle_thres = 0
    while angle_thres < 2 * np.pi:
        angle_thres += 0.08
        for x in range(81):
            for y in range(27):
                dx = x - 40
                dy = y - 13
                if dx == 0 and dy == 0:
                    board[y, x] = value
                else:
                    angle = np.arctan2(dy, dx)
                    if angle < 0:
                        angle += 2 * np.pi
                    angle = (angle * streaks) % (2 * np.pi)
                    if angle <= angle_thres:
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


def falling_columns(board, pattern, disappear):
    for x in range(pattern.shape[1]):
        if pattern[:, x].any():
            max_y = np.max(np.where(pattern[:, x]))
            for y_offset in range(max_y + 1):
                board[:, x] = False
                for y in range(pattern.shape[0]):
                    y_text = y + y_offset + 1 if disappear else y + max_y - y_offset
                    if 0 <= y_text < pattern.shape[0]:
                        board[y, x] = pattern[y_text, x]
                    else:
                        break

                time.sleep(0.015)


def floodfill(board, pattern, disappear=False, bfs=False):
    pattern = pattern.copy()
    while pattern.any():
        stack = []
        where = np.where(pattern)
        stack.append((where[0][0], where[1][0]))
        while stack:
            index = 0 if bfs else -1
            y, x = stack.pop(index)
            if pattern[y, x]:
                pattern[y, x] = False
                board[y, x] = not disappear
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if (0 <= x + dx < pattern.shape[1]) and (0 <= y + dy < pattern.shape[0]):
                            if pattern[y + dy, x + dx]:
                                stack.append((y + dy, x + dx))
            else:
                continue

            time.sleep(0.02)


def pixel_slide_in(board, pattern, disappear=False, steps=100):
    coords = np.argwhere(pattern)
    # Generate starting locs (y, x)
    start = np.empty_like(coords)
    for i in range(coords.shape[0]):
        if random.random() < 0.5:
            start[i] = (random.randint(0, board.shape[0] - 1), -5 if random.random() < 0.5 else board.shape[1] + 5)
        else:
            start[i] = (-5 if random.random() < 0.5 else board.shape[0] + 5, random.randint(0, board.shape[1] - 1))

    # Pixel specific duration
    duration = np.random.randint(int(0.7 * steps), steps, size=coords.shape[0])
    for i in range(steps):
        board[:] = False
        for j in range(coords.shape[0]):
            if i >= duration[j]:
                loc = start[j] if disappear else coords[j]
            else:
                fac = i / duration[j]
                if disappear:
                    fac = 1 - fac
                loc = (fac * coords[j] + (1 - fac) * start[j]).astype(int)
            y, x = loc
            if 0 <= y < board.shape[0] and 0 <= x < board.shape[1]:
                board[y, x] = True

        time.sleep(0.04)


# Other
def generate_border(text: np.ndarray) -> np.ndarray:
    border = np.zeros((text.shape[0], text.shape[1]), dtype=bool)
    for x in range(text.shape[1]):
        for y in range(text.shape[0]):
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if (0 <= x + dx < text.shape[1]) and (0 <= y + dy < text.shape[0]) and not (dx == 0 and dy == 0):
                        if text[y + dy, x + dx]:
                            border[y, x] = True

    border = np.logical_and(border, np.logical_not(text))
    return border


def screensaver_main(display, board):
    """
    board: ndarray shape (27, 81), dtype bool
        Shared object to indicate which dots are lit.
    """
    # Load patterns
    pat_arrniey = np.load("arrniey.npy")
    pat_boomland = np.load("boom.npy")
    pat_i = np.load("I.npy")
    pat_toast = np.load("toast.npy")
    pat_ultimate = np.load("ultimate.npy")
    pat_ulti_border = generate_border(pat_ultimate)
    pat_ulti_and_i = np.logical_and(
        np.logical_or(pat_ultimate, pat_i),
        np.logical_not(np.logical_and(pat_ulti_border, pat_i))
    )

    patterns = [
        pat_arrniey,
        pat_boomland,
        pat_i,
        pat_toast,
        pat_ultimate,
        pat_ulti_and_i,
    ]
    create_funcs = [
        #lambda p: matrix(board, np.logical_not(p)),
        #lambda p: falling_columns(board, p, disappear=False),
        lambda p: floodfill(board, p, disappear=False, bfs=random.random() < 0.5),
        lambda p: pixel_slide_in(board, p, disappear=False),
    ]
    erase_funcs = [
        #random_fill,
        #left_to_right_fill,
        #circle_fill,
        #radial_fill,
        #lambda p: falling_columns(board, p, disappear=True),
        lambda p: floodfill(board, p, disappear=True, bfs=random.random() < 0.5),
        lambda p: pixel_slide_in(board, p, disappear=True),
    ]

    while display.run:
        pattern = random.choice(patterns)
        random.choice(create_funcs)(pattern)
        time.sleep(2)

        random.choice(erase_funcs)(board)
        board[:] = False
        time.sleep(2)
