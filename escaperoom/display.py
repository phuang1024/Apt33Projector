"""
Handles rendering and warping to fit the board.

Run this file to live adjust the display field of view.
"""

import json
import os
import time

import cv2
import numpy as np
import pygame

WINDOW_RES = (424, 240)


class Display:
    def __init__(self):
        self.load_warp()

        self.keydown_callbacks = []

        self.run = True
        self.window = pygame.display.set_mode(WINDOW_RES, pygame.FULLSCREEN)

    def add_keydown_callback(self, callback):
        """
        On each pygame.KEYDOWN event, all callbacks are called with args (event.key,)
        """
        self.keydown_callbacks.append(callback)

    def start(self):
        """
        Blocking (pygame needs main thread).
        Keep updating display.
        """
        while self.run:
            time.sleep(1 / 60)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                elif event.type == pygame.KEYDOWN:
                    for callback in self.keydown_callbacks:
                        callback(event.key)
                    if event.key in (pygame.K_ESCAPE, pygame.K_q):
                        self.run = False

        pygame.quit()

    def render(self, img):
        """
        Will warp img to fit view, and display onto window.
        """
        from_pts = np.array([
            [0, 0],
            [0, img.shape[0]],
            [img.shape[1], img.shape[0]],
            [img.shape[1], 0],
        ], dtype=np.float32)
        to_pts = self.warp

        matrix = cv2.getPerspectiveTransform(from_pts, to_pts)
        warped = cv2.warpPerspective(
            img,
            matrix,
            WINDOW_RES,
        )

        warped = cv2.cvtColor(warped, cv2.COLOR_GRAY2RGB)
        warped = warped.swapaxes(0, 1)
        surface = pygame.surfarray.make_surface(warped)

        if not self.run:
            print("Warning: render() called when display not running.")
            return

        self.window.blit(surface, (0, 0))

    def load_warp(self):
        if os.path.isfile("warp.json"):
            with open("warp.json", "r") as f:
                self.warp = json.load(f)
        else:
            print("Warning: No warp.json found.")
            self.warp = (
                [0, 0],
                [0, WINDOW_RES[1]],
                [WINDOW_RES[0], WINDOW_RES[1]],
                [WINDOW_RES[0], 0],
            )
        self.warp = np.array(self.warp, dtype=np.float32)

    def save_warp(self):
        with open("warp.json", "w") as f:
            json.dump(self.warp.tolist(), f, indent=4)
