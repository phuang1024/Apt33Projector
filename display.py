"""
Implementation of pygame and display math.
"""

import json
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
    x_ival = 12 * 3**0.5 / 2
    y_ival = 12
    x_offset = 0
    y_offset = 0
    radius = 4
    rotation = 0
    x_persp = 0
    y_persp = 0
    x_stretch = 0

    attrs = [
        "x_ival",
        "y_ival",
        "x_offset",
        "y_offset",
        "radius",
        "rotation",
        "x_persp",
        "y_persp",
        "x_stretch",
    ]

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
            self.params.load("disp.json")

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

        total_width = 81 * params.x_ival
        total_height = 27 * params.y_ival
        offset_x = (width - total_width) / 2 + params.x_offset
        offset_y = (height - total_height) / 2 + params.y_offset

        raw_img = np.zeros((height, width, 3), dtype=np.uint8)
        for grid_x in range(81):
            px_x = grid_x * params.x_ival + np.sin(grid_x / 40 * np.pi) * params.x_stretch + offset_x
            for grid_y in range(27):
                px_y = grid_y * params.y_ival + offset_y
                if grid_x % 2 == 0:
                    px_y += params.y_ival // 2

                color = (255, 255, 255) if self.board[grid_y, grid_x] else (0, 0, 0)
                cv2.circle(raw_img, (int(px_x), int(px_y)), int(params.radius), color, -1, cv2.LINE_AA)

        # Warp perspective
        from_pts = np.array([
            [0, 0],
            [width, 0],
            [0, height],
            [width, height]
        ], dtype=np.float32)
        to_pts = np.array([
            [-params.x_persp, -params.y_persp],
            [width + params.x_persp, params.y_persp],
            [params.x_persp, height + params.y_persp],
            [width - params.x_persp, height - params.y_persp]
        ], dtype=np.float32)
        trans = cv2.getPerspectiveTransform(from_pts, to_pts)
        img = cv2.warpPerspective(raw_img, trans, (width, height))

        trans_rot = cv2.getRotationMatrix2D((width // 2, height // 2), params.rotation, 1)
        img = cv2.warpAffine(img, trans_rot, (width, height))

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img.swapaxes(0, 1)
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
