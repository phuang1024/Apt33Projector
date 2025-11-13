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

# Doesn't matter bc full screen.
WINDOW_RES = (1920, 1080)


class Display:
    def __init__(self):
        self.load_view_coords()

        self.window = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)

    def start(self):
        """
        Blocking (pygame needs main thread).
        Keep updating display.
        """
        run = True

        while run:
            time.sleep(1 / 60)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

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
        to_pts = self.view_coords

        matrix = cv2.getPerspectiveTransform(from_pts, to_pts)
        warped = cv2.warpPerspective(
            img,
            matrix,
            WINDOW_RES,
        )

        surface = pygame.surfarray.make_surface(
            cv2.cvtColor(warped, cv2.COLOR_BGR2RGB).swapaxes(0, 1)
        )
        self.window.blit(surface, (0, 0))

    def load_view_coords(self):
        if os.path.isfile("view_coords.json"):
            with open("view_coords.json", "r") as f:
                self.view_coords = json.load(f)
        else:
            print("Warning: No view_coords.json found.")
            self.view_coords = (
                [0, 0],
                [0, WINDOW_RES[1]],
                [WINDOW_RES[0], WINDOW_RES[1]],
                [WINDOW_RES[0], 0],
            )
        self.view_coords = np.array(self.view_coords, dtype=np.float32)
