"""
Display text on the board.
"""

import argparse

import numpy as np
import pygame

from display import Display


def draw_daemon(disp: Display, text):
    aspect = 81 / 27
    x_size = int(text.shape[1] * aspect)
    zeros = np.zeros((text.shape[0], x_size - text.shape[1]), dtype=np.uint8)
    text = np.concatenate


def main():
    disp = Display()
    disp.start()


if __name__ == "__main__":
    main()
