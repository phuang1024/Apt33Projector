"""
Play snake game.
"""

import argparse
import random
import time

import numpy as np
import pygame

from display import Display
from screensaver import erase
from text import draw_text

game_running = True
# 0 up, 1 right, 2 down, 3 left
snake_dir = 1
food_loc = None
global_iter = 0
keypress_iter = 0

DEFAULT_SNAKE = np.array([[5, 5], [6, 5], [7, 5]])


def set_snake_dir(dir: int):
    """
    Makes sure dir does not reverse.
    """
    global snake_dir
    if dir == 0 and snake_dir != 2:
        snake_dir = 0
    elif dir == 1 and snake_dir != 3:
        snake_dir = 1
    elif dir == 2 and snake_dir != 0:
        snake_dir = 2
    elif dir == 3 and snake_dir != 1:
        snake_dir = 3


def key_handler(disp: Display, key: str):
    global snake_dir, keypress_iter
    if keypress_iter == global_iter:
        return
    keypress_iter = global_iter
    if key == pygame.K_UP:
        set_snake_dir(0)
    elif key == pygame.K_RIGHT:
        set_snake_dir(1)
    elif key == pygame.K_DOWN:
        set_snake_dir(2)
    elif key == pygame.K_LEFT:
        set_snake_dir(3)


def snake_daemon(disp: Display, auto: bool):
    global game_running, food_loc, snake_dir, global_iter

    period = 0.1

    # Prioritize X or Y
    auto_priority = random.randint(0, 1)

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
            food_loc = np.array([np.random.randint(4, disp.board.shape[1] - 5), np.random.randint(4, disp.board.shape[0] - 5)])
            last_food_time = time.time()

        delta = [(0, -1), (1, 0), (0, 1), (-1, 0)][snake_dir]
        if (snake[-1] == food_loc).all():
            snake = np.append(snake, [snake[-1] + delta], axis=0)
            food_loc = None
            period *= 0.97
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

        if auto:
            if food_loc is not None:
                if auto_priority == 0:
                    if snake[-1][0] == food_loc[0]:
                        set_snake_dir(2 if snake[-1][1] < food_loc[1] else 0)
                    else:
                        set_snake_dir(1 if snake[-1][0] < food_loc[0] else 3)
                else:
                    if snake[-1][1] == food_loc[1]:
                        set_snake_dir(1 if snake[-1][0] < food_loc[0] else 3)
                    else:
                        set_snake_dir(2 if snake[-1][1] < food_loc[1] else 0)

            if snake[-1][0] <= 2 and snake_dir == 3:
                set_snake_dir(random.choice([0, 2]))
            if snake[-1][1] <= 2 and snake_dir == 0:
                set_snake_dir(random.choice([1, 3]))
            if snake[-1][0] >= disp.board.shape[1] - 3 and snake_dir == 1:
                set_snake_dir(random.choice([0, 2]))
            if snake[-1][1] >= disp.board.shape[0] - 3 and snake_dir == 2:
                set_snake_dir(random.choice([1, 3]))

            if random.random() < 0.1:
                auto_priority = random.randint(0, 1)

        global_iter += 1
        time.sleep(period)


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
    parser = argparse.ArgumentParser()
    parser.add_argument("--auto", action="store_true")
    args = parser.parse_args()

    disp = Display()
    if not args.auto:
        disp.keydown_hooks.append(key_handler)
    disp.add_daemon(snake_daemon, (disp, args.auto))
    disp.add_daemon(food_daemon, (disp,))
    disp.start()


if __name__ == "__main__":
    main()
