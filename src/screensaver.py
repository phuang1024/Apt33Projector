"""
Cool repeating text animations of Ultimate and I.
"""

import argparse
import math
import random
import time

import numpy as np

from display import Display


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


def erase(disp: Display, fill=False):
    coords = [(x, y) for x in range(disp.board.shape[1]) for y in range(disp.board.shape[0])]

    choice = random.random()
    if choice < 0.25:
        # Sweep erase
        for x in range(disp.board.shape[1]):
            for y in range(disp.board.shape[0]):
                disp.board[y, x] = fill
                time.sleep(0.002)
                if not disp.run:
                    return

    elif choice < 0.5:
        # Random erase
        coords.sort(key=lambda x: random.random())
        for x, y in coords:
            disp.board[y, x] = fill
            time.sleep(0.002)
            if not disp.run:
                return

    elif choice < 0.75:
        # Radial erase
        coords.sort(key=lambda x: math.hypot(x[0] - disp.board.shape[1] // 2, x[1] - disp.board.shape[0] // 2))
        for x, y in coords:
            disp.board[y, x] = fill
            time.sleep(0.002)
            if not disp.run:
                return

    else:
        num_streaks = random.randint(1, 5)
        angle_thres = 0
        while True:
            for x in range(disp.board.shape[1]):
                for y in range(disp.board.shape[0]):
                    angle = math.atan2(y - disp.board.shape[0] // 2, x - disp.board.shape[1] // 2)
                    angle = ((angle * num_streaks) % (2 * math.pi)) / num_streaks
                    if angle < angle_thres:
                        disp.board[y, x] = fill
            angle_thres += 0.05
            time.sleep(0.05)
            if not disp.run:
                return

            if fill and disp.board.all():
                break
            if not fill and not disp.board.any():
                break


def falling_columns(disp: Display, text, interval=0.02, disappear=False):
    for x in range(text.shape[1]):
        if text[:, x].any():
            max_y = np.max(np.where(text[:, x]))
            for y_offset in range(max_y + 1):
                disp.board[:, x] = False
                for y in range(text.shape[0]):
                    y_text = y + y_offset + 1 if disappear else y + max_y - y_offset
                    if 0 <= y_text < text.shape[0]:
                        disp.board[y, x] = text[y_text, x]
                    else:
                        break
                if not disp.run:
                    return
                time.sleep(interval)


def floodfill(disp: Display, text, interval=0.03, disappear=False, bfs=False):
    text = text.copy()
    while text.any():
        stack = []
        where = np.where(text)
        stack.append((where[0][0], where[1][0]))
        while stack:
            index = 0 if bfs else -1
            y, x = stack.pop(index)
            if text[y, x]:
                text[y, x] = False
                disp.board[y, x] = not disappear
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if (0 <= x + dx < text.shape[1]) and (0 <= y + dy < text.shape[0]):
                            if text[y + dy, x + dx]:
                                stack.append((y + dy, x + dx))
            else:
                continue
            time.sleep(interval)
            if not disp.run:
                return


def matrix(disp: Display, text_negative, interval=0.05):
    source = np.zeros([disp.board.shape[1]], dtype=int)
    image = np.zeros_like(disp.board, dtype=bool)
    density = 0.05

    total_iters = random.randint(200, 400)
    for i in range(total_iters):
        if i >= total_iters - disp.board.shape[0] - 5:
            density = 1
        else:
            if random.random() < 0.02:
                density = random.uniform(0.01, 0.1)

        image = np.roll(image, 1, axis=0)
        image[0, :] = False
        for x in range(len(source)):
            if source[x] > 0:
                image[0, x] = True
            source[x] = max(0, source[x] - 1)
            if random.random() < density:
                source[x] = random.randint(2, 5)

        disp.board = np.logical_and(image, np.logical_not(text_negative))
        time.sleep(interval)
        if not disp.run:
            return


def text(disp: Display):
    ulti = np.load("ultimate.npy")
    illinois = np.load("I.npy")
    toast = np.load("toast.npy")
    boom = np.load("boom.npy")
    ulti_border = generate_border(ulti)
    ulti_and_i = np.logical_and(np.logical_or(ulti, illinois), np.logical_not(np.logical_and(ulti_border, illinois)))

    matrix_masks = [
        ulti, illinois, ulti_and_i, ulti_border,
        toast, boom,
        np.zeros_like(ulti, dtype=bool)
    ]
    text_masks = [
        ulti, illinois, ulti_and_i, ulti_border,
        toast, boom,
        np.logical_xor(ulti, illinois)
    ]

    while disp.run:
        if random.random() < 0.5:
            mask = random.choice(matrix_masks)
            matrix(disp, mask)
            time.sleep(2)
            erase(disp)
        else:
            text = random.choice(text_masks)
            floodfill(disp, text, bfs=random.random() < 0.5)
            time.sleep(2)
            if random.random() < 0.5:
                floodfill(disp, text, disappear=True, bfs=random.random() < 0.5)
            else:
                erase(disp)

        time.sleep(2)


def main():
    disp = Display()
    disp.add_daemon(text, (disp,))
    disp.start()


if __name__ == "__main__":
    main()
