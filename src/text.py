"""
Display text on the board.
"""

import argparse
import os
import random
import time

import cv2
import numpy as np
import pygame

from display import Display

DEFAULT_FONT = "./Aldrich-Regular.ttf"


def render_text(text, font=None):
    """
    Render text as boolean array.
    Vertical size equal to disp.board vertical size.
    Horziontal size variable.
    """
    if font is None:
        font = DEFAULT_FONT
    if os.path.isfile(font):
        font = pygame.font.Font(font, 24)
    else:
        font = pygame.font.SysFont(font, 24)

    if len(text) == 0:
        text = np.zeros((23, 1), dtype=bool)
    else:
        text_transparent = font.render(text, True, (255, 255, 255))
        text = pygame.Surface(text_transparent.get_size())
        text.fill((0, 0, 0))
        text.blit(text_transparent, (0, 0))
        text = pygame.surfarray.array3d(text).mean(axis=2).astype(np.uint8).swapaxes(0, 1)
        text = cv2.resize(text, (int(text.shape[1] / text.shape[0] * 23 * 0.7), 23))

    padding = np.zeros((2, text.shape[1]), dtype=bool)
    text = np.concatenate((padding, text, padding), axis=0)
    text = text > 128

    return text


def draw_scrolling_text(disp: Display, text, font=None):
    """
    Draw text that scrolls across screen.
    """
    text = render_text(text, font=font)

    # Pad zeros horizontally on both sides
    zeros = np.zeros((27, 85), dtype=bool)
    text = np.concatenate((zeros, text, zeros), axis=1)

    # Scrolling display
    for i in range(0, text.shape[1] - disp.board.shape[1], 2):
        disp.board[:] = text[:, i : i + disp.board.shape[1]]
        time.sleep(0.07)
        if not disp.run:
            break


def draw_daemon(disp: Display, args):
    if args.file is not None:
        with open(args.file, "r") as f:
            lines = f.readlines()
        if args.shuffle:
            random.shuffle(lines)
        while disp.run:
            for line in lines:
                draw_scrolling_text(disp, line.strip(), args.font)
            if not args.repeat:
                break

    elif args.text is not None:
        while disp.run:
            draw_scrolling_text(disp, args.text, args.font)
            if not args.repeat:
                break


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", type=str, help="Manually set single text.")
    parser.add_argument("--file", type=str, help="Display from file.")
    parser.add_argument("--shuffle", action="store_true", help="Whether to shuffle contents of file.")
    parser.add_argument("--repeat", action="store_true")
    parser.add_argument("--font", type=str)
    parser.add_argument("--limit", type=float)
    args = parser.parse_args()

    disp = Display(time_limit=args.limit)
    disp.add_daemon(draw_daemon, (disp, args))
    disp.start()


if __name__ == "__main__":
    main()
