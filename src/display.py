"""
Implementation of pygame and display math.
"""

import json
import os
import time
from threading import Thread

import cv2
import numpy as np
import pygame

pygame.init()


class DrawParams:
    """
    Constants for board projection.
    """
    radius: float
    # (y, x) positions
    tl: tuple[float, float]
    tr: tuple[float, float]
    br: tuple[float, float]
    bl: tuple[float, float]

    attrs = [
        "radius",
        "tl",
        "tr",
        "br",
        "bl",
    ]

    def __init__(self):
        self.radius = 3
        self.tl = (100, 100)
        self.tr = (100, 715)
        self.br = (300, 715)
        self.bl = (300, 100)

    def save(self, path):
        data = {}
        for attr in self.attrs:
            data[attr] = getattr(self, attr)
        with open(path, "w") as f:
            json.dump(data, f, indent=4)

    def load(self, path):
        with open(path, "r") as f:
            data = json.load(f)
        for attr in self.attrs:
            if attr in data:
                setattr(self, attr, data[attr])


class Display:
    def __init__(self, load_params=True):
        self.board = np.zeros((27, 81), dtype=bool)
        self.run = True

        self.window = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN)
        self.params = DrawParams()
        if load_params:
            if os.path.isfile("disp.json"):
                self.params.load("disp.json")
            else:
                print("Warning: disp.json not found")

        self.daemons = []
        # Append to this externally. Each func is called with (self, event.key)
        self.keydown_hooks = []

    def save_board(self, path):
        np.save(path, self.board)

    def load_board(self, path):
        self.board = np.load(path)

    def start(self):
        """
        Blocking (pygame needs main thread).
        """
        while self.run:
            time.sleep(1 / 140)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_ESCAPE, pygame.K_q):
                        self.run = False
                    for hook in self.keydown_hooks:
                        hook(self, event.key)

            self.draw_board()
            pygame.display.flip()

        pygame.quit()
        for daemon in self.daemons:
            daemon.join()

    def draw_board(self):
        params = self.params
        width = self.window.get_width()
        height = self.window.get_height()

        y_ival = 9
        x_ival = y_ival * 3**0.5 / 2
        total_width = 81 * x_ival
        total_height = 27 * y_ival
        offset_x = (width - total_width) / 2
        offset_y = (height - total_height) / 2

        raw_img = np.zeros((height, width, 3), dtype=np.uint8)
        for grid_x in range(81):
            px_x = grid_x * x_ival + offset_x
            for grid_y in range(27):
                px_y = grid_y * y_ival + offset_y
                if grid_x % 2 == 0:
                    px_y += y_ival // 2

                color = (255, 255, 255) if self.board[grid_y, grid_x] else (0, 0, 0)
                cv2.circle(raw_img, (int(px_x), int(px_y)), int(params.radius), color, -1, cv2.LINE_AA)

        # Warp perspective
        min_x = offset_x
        max_x = 80 * x_ival + offset_x
        min_y = offset_y
        max_y = 26 * y_ival + offset_y
        from_pts = np.array([
            [min_x, min_y],
            [max_x, min_y],
            [max_x, max_y],
            [min_x, max_y],
        ], dtype=np.float32)
        to_pts = np.array([params.tl, params.tr, params.br, params.bl], dtype=np.float32)
        trans = cv2.getPerspectiveTransform(from_pts, to_pts)
        img = cv2.warpPerspective(raw_img, trans, (height, width))

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        #img = img.swapaxes(0, 1)
        img = pygame.surfarray.make_surface(img)
        self.window.blit(img, (0, 0))

    def add_daemon(self, func, args):
        """
        Handles creating and starting thread, and joining at end of self.start()
        """
        daemon = Thread(target=func, args=args)
        daemon.start()
        self.daemons.append(daemon)
        return daemon
