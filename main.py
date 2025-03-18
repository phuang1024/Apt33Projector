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


def update_daemon(board, run):
    """
    run: List with one element; first element is True/False.
    """
    while run[0]:
        time.sleep(1)

        board[:] = np.random.randint(0, 2, size=board.shape, dtype=bool)


def draw_board(window, board: np.ndarray):
    """
    board: Array shape (27, 81)
    """
    window.fill((0, 0, 0))

    for grid_x in range(81):
        px_x = grid_x * X_INTERVAL + OFFSET[0]
        for grid_y in range(27):
            px_y = grid_y * Y_INTERVAL + OFFSET[1]
            if grid_x % 2 == 0:
                px_y += Y_INTERVAL // 2
            color = (255, 255, 255) if board[grid_y, grid_x] else (0, 0, 0)
            pygame.gfxdraw.filled_circle(window, int(px_x), int(px_y), RADIUS, color)
            pygame.gfxdraw.aacircle(window, int(px_x), int(px_y), RADIUS, color)


def main():
    board = np.zeros((27, 81), dtype=bool)
    # Using list for mutability
    run = [True]

    daemon = Thread(target=update_daemon, args=(board, run))
    daemon.start()

    window = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN)

    while run[0]:
        time.sleep(1 / 60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run[0] = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    run[0] = False

        draw_board(window, board)
        pygame.display.flip()

    pygame.quit()
    daemon.join()


if __name__ == "__main__":
    main()
