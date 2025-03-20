"""
Play snake game.
"""

import time

import numpy as np
import pygame

from display import Display
from screensaver import erase
from text import draw_text

# 0 up, 1 right, 2 down, 3 left
game_running = True
snake_dir = 1
food_loc = None
global_iter = 0
keypress_iter = 0

DEFAULT_SNAKE = np.array([[5, 5], [6, 5], [7, 5]])


def key_handler(disp: Display, key: str):
    global snake_dir, keypress_iter
    if keypress_iter == global_iter:
        return
    keypress_iter = global_iter
    if key == pygame.K_UP and snake_dir != 2:
        snake_dir = 0
    elif key == pygame.K_RIGHT and snake_dir != 3:
        snake_dir = 1
    elif key == pygame.K_DOWN and snake_dir != 0:
        snake_dir = 2
    elif key == pygame.K_LEFT and snake_dir != 1:
        snake_dir = 3


def snake_daemon(disp: Display):
    global game_running, food_loc, snake_dir, global_iter

    # Head last
    snake = DEFAULT_SNAKE.copy()
    last_food_time = time.time()
    while disp.run:
        # Highlight border
        disp.board[0, :] = True
        disp.board[-1, :] = True
        disp.board[:, 0] = True
        disp.board[:, -1] = True

        if time.time() - last_food_time > 10 or food_loc is None:
            if food_loc is not None:
                disp.board[food_loc[1], food_loc[0]] = False
            food_loc = np.array([np.random.randint(3, disp.board.shape[1] - 3), np.random.randint(3, disp.board.shape[0] - 3)])
            last_food_time = time.time()

        delta = [(0, -1), (1, 0), (0, 1), (-1, 0)][snake_dir]
        if (snake[-1] == food_loc).all():
            snake = np.append(snake, [snake[-1] + delta], axis=0)
            food_loc = None
        else:
            disp.board[snake[0][1], snake[0][0]] = False
            new_head = snake[-1] + delta
            snake = np.roll(snake, -1, axis=0)
            snake[-1] = new_head

        clean = False
        if 0 <= snake[-1][0] < disp.board.shape[1] and 0 <= snake[-1][1] < disp.board.shape[0]:
            for i in range(len(snake) - 1):
                if (snake[i] == snake[-1]).all():
                    break
            else:
                clean = True
        if clean:
            disp.board[snake[-1][1], snake[-1][0]] = True
        else:
            game_running = False

            time.sleep(1)
            erase(disp, fill=True)
            time.sleep(1)
            disp.board[:] = False
            draw_text(disp, "helvetica", f"YOUR SCORE: {len(snake)}")

            snake = DEFAULT_SNAKE.copy()
            snake_dir = 1
            game_running = True

        global_iter += 1
        time.sleep(0.1)


def food_daemon(disp: Display):
    global food_loc
    while disp.run:
        if food_loc is not None and game_running:
            tmp = food_loc.copy()
            disp.board[tmp[1], tmp[0]] = False
            time.sleep(0.2)
            disp.board[tmp[1], tmp[0]] = True
        time.sleep(0.32)


def main():
    disp = Display()
    disp.keydown_hooks.append(key_handler)
    disp.add_daemon(snake_daemon, (disp,))
    disp.add_daemon(food_daemon, (disp,))
    disp.start()


if __name__ == "__main__":
    main()
