import argparse
import curses
import random
import time


def main(stdscr, demo=False):
    curses.curs_set(0)
    sh, sw = stdscr.getmaxyx()
    win = curses.newwin(sh, sw, 0, 0)
    win.keypad(1)
    win.nodelay(1)
    win.timeout(100)

    # initial snake position
    snk_x = sw // 4
    snk_y = sh // 2
    snake = [[snk_y, snk_x], [snk_y, snk_x - 1], [snk_y, snk_x - 2]]

    # initial food
    food = [sh // 2, sw // 2]
    win.addch(food[0], food[1], curses.ACS_PI)

    key = curses.KEY_RIGHT
    frames = 0
    max_frames = 60 if demo else float("inf")

    while True:
        next_key = win.getch()
        if next_key != -1:
            key = next_key

        if demo:
            frames += 1
            if frames >= max_frames:
                break

        y = snake[0][0]
        x = snake[0][1]
        if key == curses.KEY_DOWN:
            y += 1
        elif key == curses.KEY_UP:
            y -= 1
        elif key == curses.KEY_LEFT:
            x -= 1
        elif key == curses.KEY_RIGHT:
            x += 1

        snake.insert(0, [y, x])

        if y in [0, sh - 1] or x in [0, sw - 1] or snake[0] in snake[1:]:
            break

        if snake[0] == food:
            while True:
                nf = [random.randint(1, sh - 2), random.randint(1, sw - 2)]
                if nf not in snake:
                    food = nf
                    break
            win.addch(food[0], food[1], curses.ACS_PI)
        else:
            tail = snake.pop()
            win.addch(tail[0], tail[1], " ")

        win.addch(snake[0][0], snake[0][1], curses.ACS_CKBOARD)

    time.sleep(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple terminal snake game")
    parser.add_argument("--demo", action="store_true", help="run an automatic short demo")
    args = parser.parse_args()
    curses.wrapper(main, demo=args.demo)
