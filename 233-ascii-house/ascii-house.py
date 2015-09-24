import sys
import random

# Building blocks of blueprint
BP_AIR = ' '
BP_THERE = '*'
BP_AIR_PAIR = (BP_AIR, BP_AIR)
BP_BLANK_LINE = BP_AIR * 30  # maximum of 30 characters


def get_int(current):
    if current == BP_THERE:
        if random.random() < 0.5:
            return ' o '
    return ' ' * 3


def get_wall(current, previous):
    if current == previous:
        return ' '
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


def add_door(line, bp_width):
    door_pos = 4 * random.randrange(bp_width) + 1
    return line[:door_pos] + '| |' + line[(door_pos+3):]


def make_roofs(line, roofs):
    for roof in roofs:
        roof[0] += 1
        roof[1] -= 1
        if roof[1] == roof[0]:
            line = line[:roof[0]] + 'A' + line[roof[0] + 1:]
        elif roof[0] < roof[1]:
            line = line[:roof[0]] + '/' + line[roof[0] + 1:]
            line = line[:roof[1]] + '\\' + line[roof[1] + 1:]
    return line


def add_roofs(house):
    roofs = []
    roofed_house = house[:2]
    for line in house[2:]:
        roofed_house.append(make_roofs(line, roofs))
        edges = [index for index in range(len(line)) if line[index] == '+']
        roofs += [[edges[index], edges[index + 1]] for index in range(0, len(edges), 2)]
    while roofs:
        roofs = filter(lambda roof: roof[0] < roof[1], roofs)
        roofed_house.append(make_roofs(BP_BLANK_LINE * 5, roofs))
    return roofed_house


def house_from_blueprint(blueprint):
    house = []
    prev_line = BP_BLANK_LINE
    for line in [line.ljust(len(blueprint[-1])) for line in blueprint][::-1]:
        house.append(make_ceiling(zip(line, prev_line), BP_AIR_PAIR))
        house.append(make_walls(line, BP_AIR))
        prev_line = line
    house.append(make_ceiling(zip(BP_BLANK_LINE, prev_line), BP_AIR_PAIR))
    house[1] = add_door(house[1], len(blueprint[-1]))
    house = add_roofs(house)
    return house[::-1]


def make_house(file):
    with open(file, 'r') as f:
        house = house_from_blueprint(f.read().splitlines()[1:])
    for line in house:
        print line


make_house(sys.argv[1])
