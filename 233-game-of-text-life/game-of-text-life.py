import sys
import random

DEAD_CELL = ' '
DIRS = [(x, y) for x in (-1, 0, 1) for y in (-1, 0, 1) if (x, y) != (0, 0)]


def get_initial(fromfile):
    with open(fromfile, 'r') as f:
        input = f.read().splitlines()
        width = max([len(line) for line in input])
        return [line.ljust(width) for line in input]


def get_neighbours(board, x, y):
    height, width = len(board), len(board[0])  # all lines of same length
    return [board[y + dy][x + dx] for dx, dy in DIRS
            if (y + dy) in range(height) and (x + dx) in range(width)]


def get_new_state(cell, neighbours):
    alive_neighbours = list(filter(lambda x: x != DEAD_CELL, neighbours))
    if cell == DEAD_CELL:
        if len(alive_neighbours) == 3:
            return random.choice(alive_neighbours)
        else:
            return DEAD_CELL
    else:
        if len(alive_neighbours) in [2, 3]:
            return cell
        else:
            return DEAD_CELL


def do_step(board):
    return [[get_new_state(cell, get_neighbours(board, x, y))
             for x, cell in enumerate(line)] for y, line in enumerate(board)]


for line in do_step(get_initial(sys.argv[1])):
    print(''.join(line))
