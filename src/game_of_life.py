"""
Testing script: Random black and white pixels
"""

import argparse
import time

import numpy as np

from display import Display


def game_step(board):
    """
    board: Modifies in place.
    """
    old_board = board.copy()
    for y in range(board.shape[0]):
        for x in range(board.shape[1]):
            neighbors = 0
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    if 0 <= x + dx < board.shape[1] and 0 <= y + dy < board.shape[0]:
                        neighbors += old_board[y + dy, x + dx]
            if old_board[y, x] == 1:
                if neighbors < 2 or neighbors > 3:
                    board[y, x] = 0
            else:
                if neighbors == 3:
                    board[y, x] = 1


def game_daemon(disp: Display):
    iters = 1e9
    while disp.run:
        if iters > 150:
            iters = 0
            disp.board[:] = np.random.randint(0, 2, size=(disp.board.shape[0], disp.board.shape[1])) == 0
        game_step(disp.board)
        iters += 1
        time.sleep(0.1)


def main():
    disp = Display()
    disp.add_daemon(game_daemon, (disp,))
    disp.start()


if __name__ == "__main__":
    main()
