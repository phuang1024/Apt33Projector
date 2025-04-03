"""
Clock.
"""

import argparse
import time
from datetime import datetime

import numpy as np

from display import Display
from text import render_text


def clock_daemon(disp: Display):
    while disp.run:
        now = datetime.now()
        text = now.strftime("%H:%M:%S")
        if time.time() % 1 < 0.5:
            text = text.replace(":", " ")

        text = render_text(text)
        disp.board[:] = False
        pad = (81 - text.shape[1]) // 2
        disp.board[:, pad : pad + text.shape[1]] = text

        time.sleep(0.05)


def main():
    disp = Display()
    disp.add_daemon(clock_daemon, (disp,))
    disp.start()


if __name__ == "__main__":
    main()
