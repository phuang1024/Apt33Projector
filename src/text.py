"""
Display text on the board.
"""

import argparse
import random
import time

import cv2
import numpy as np
import pygame

from display import Display


def draw_text(disp: Display, font, text):
    """
    Draw text that scrolls across screen.
    """
    font = pygame.font.SysFont(font, 24)
    text_transparent = font.render(text, True, (255, 255, 255))
    text = pygame.Surface(text_transparent.get_size())
    text.fill((0, 0, 0))
    text.blit(text_transparent, (0, 0))
    text = pygame.surfarray.array3d(text).mean(axis=2).astype(np.uint8).swapaxes(0, 1)

    text = cv2.resize(text, (int(text.shape[1] / text.shape[0] * 23 * 0.7), 23))
    padding = np.zeros((2, text.shape[1]), dtype=bool)
    text = np.concatenate((padding, text, padding), axis=0)
    text = text > 128

    # Pad zeros horizontally on both sides
    zeros = np.zeros((27, 85), dtype=bool)
    text = np.concatenate((zeros, text, zeros), axis=1)

    # Scrolling display
    for i in range(text.shape[1] - disp.board.shape[1]):
        disp.board[:] = text[:, i : i + disp.board.shape[1]]
        time.sleep(0.03)
        if not disp.run:
            break


def draw_daemon(disp: Display, args):
    if args.file is not None:
        with open(args.file, "r") as f:
            lines = f.readlines()
        random.shuffle(lines)
        while disp.run:
            for line in lines:
                draw_text(disp, args.font, line.strip())

    elif args.text is not None:
        while disp.run:
            draw_text(disp, args.font, args.text)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", type=str, help="Manually set single text.")
    parser.add_argument("--file", type=str, help="Display sequentially from file.")
    parser.add_argument("--font", type=str, default="arial")
    args = parser.parse_args()

    disp = Display()
    disp.add_daemon(draw_daemon, (disp, args))
    disp.start()


if __name__ == "__main__":
    main()
