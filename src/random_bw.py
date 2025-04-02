"""
Testing script: Random black and white pixels
"""

import argparse
import time

import numpy as np

from display import Display


def random_bw(disp: Display):
    while disp.run:
        time.sleep(1)
        disp.board[:] = np.random.randint(0, 2, size=disp.board.shape, dtype=bool)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=float)
    args = parser.parse_args()

    disp = Display(time_limit=args.limit)
    disp.add_daemon(random_bw, (disp,))
    disp.start()


if __name__ == "__main__":
    main()
