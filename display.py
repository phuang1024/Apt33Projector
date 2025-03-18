import time
from threading import Thread

import numpy as np
import pygame
import pygame.gfxdraw

pygame.init()

# Constants for board projection
X_INTERVAL = 12 * 3**0.5 / 2
Y_INTERVAL = 12
OFFSET = (50, 50)
RADIUS = 4


class Display:
    def __init__(self):
        self.board = np.zeros((27, 81), dtype=bool)
        self.run = True

        self.window = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN)

        self.daemons = []

    def start(self):
        """
        Blocking (pygame needs main thread).
        """
        while self.run:
            time.sleep(1 / 60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_ESCAPE, pygame.K_q):
                        self.run = False

            self.draw_board()
            pygame.display.flip()

        pygame.quit()
        for daemon in self.daemons:
            daemon.join()

    def draw_board(self):
        self.window.fill((0, 0, 0))

        for grid_x in range(81):
            px_x = grid_x * X_INTERVAL + OFFSET[0]
            for grid_y in range(27):
                px_y = grid_y * Y_INTERVAL + OFFSET[1]
                if grid_x % 2 == 0:
                    px_y += Y_INTERVAL // 2
                color = (255, 255, 255) if self.board[grid_y, grid_x] else (0, 0, 0)
                pygame.gfxdraw.filled_circle(self.window, int(px_x), int(px_y), RADIUS, color)
                pygame.gfxdraw.aacircle(self.window, int(px_x), int(px_y), RADIUS, color)

    def add_daemon(self, func, args):
        """
        Handles creating and starting thread, and joining at end of self.start()
        """
        daemon = Thread(target=func, args=args)
        daemon.start()
        self.daemons.append(daemon)
        return daemon
