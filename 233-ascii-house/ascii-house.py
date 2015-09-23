import sys
import random

# Building blocks of blueprint
BP_AIR = ' '
BP_THERE = '*'
BP_AIR_PAIR = (BP_AIR, BP_AIR)
BP_BLANK_LINE = ' ' * 30  # maximum of 30 characters


def get_int(current):
    if current == BP_THERE:
        if random.random() >= 0.5:
            return ' o '
    return ' ' * 3


def get_wall(current, previous):
    if current == previous:
        return ' '
    else:
        return '|'


def make_walls(bp_line, previous):
    if bp_line == '':
        return get_wall(BP_AIR, previous)
    else:
        return (get_wall(bp_line[0], previous) + get_int(bp_line[0]) +
                make_walls(bp_line[1:], bp_line[0]))


def get_line(pair):
    if pair[0] == pair[1]:
        return ' ' * 3
    return '-' * 3


def get_edge(current, previous):
    if current == previous:
        if current[0] == current[1]:
            return ' '  # air or interior
        else:
            return '-'  # continuing ceiling
    else:
        if (current[0] == current[1]) and (previous[0] == previous[1]):
            return '|'  # tower wall
        else:
            return '+'  # actual edge


def make_ceiling(vert_pairs, prev_pair):
    if vert_pairs == []:
        return get_edge(BP_AIR_PAIR, prev_pair)
    else:
        return (get_edge(vert_pairs[0], prev_pair) + get_line(vert_pairs[0]) +
                make_ceiling(vert_pairs[1:], vert_pairs[0]))


def clean_blueprint(blueprint):
    bp_width = len(blueprint[-1])
    clean_bp = [BP_BLANK_LINE]
    clean_bp.extend([line.ljust(bp_width) for line in blueprint])
    return clean_bp[::-1]


def house_from_blueprint(blueprint):
    house = []
    prev_line = BP_BLANK_LINE
    for line in clean_blueprint(blueprint):
        house.append(make_ceiling(zip(line, prev_line), BP_AIR_PAIR))
        house.append(make_walls(line, BP_AIR))
        prev_line = line
    return house[::-1]
#    return house


def make_house(file):
    with open(file, 'r') as f:
        house = house_from_blueprint(f.read().splitlines()[1:])
    for line in house:
        print line


make_house(sys.argv[1])
