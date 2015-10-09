WIDTH = 5
HEIGHT = 11


def find_solutions(tiles, free, so_far=None):
    so_far = {} if not so_far else so_far
    if not free:
        return [so_far]
    solutions = []
    spot = min(free)
    free_shifted = {(p[0] - spot[0], p[1] - spot[1]) for p in free}
    # Find all possile placements for the next tile
    for key in tiles.keys() - so_far.keys():
        for tile in tiles[key]:
            if tile.issubset(free_shifted):
                so_far[key] = {(spot[0] + p[0], spot[1] + p[1]) for p in tile}
                solutions += find_solutions(tiles, free - so_far[key], so_far)
                del so_far[key]
    return solutions


# The tiles dictionary has one entry per tile. Each entry is a list of
# tile orientations in ascii. At first, it contains only the tile and its
# flipped variations
tiles = {tile.lstrip()[0]:
         {tile, '\n'.join(tile.splitlines()[::-1]),
          '\n'.join([line[::-1] for line in tile.splitlines()]),
          '\n'.join([line[::-1] for line in tile.splitlines()[::-1]])}
         for tile in open('tiles.txt').read().split('\n\n')}

# Adding 90 degree rotated orientations
for t in tiles.values():
    t.update(['\n'.join([''.join(l) for l in zip(*tile.splitlines())][::-1])
             for tile in t.copy()])

numeric_tiles = {k: [{(line[0], char[0] - tile.splitlines()[0].index(k))
                      for line in enumerate(tile.splitlines())
                      for char in enumerate(line[1]) if char[1] != ' '}
                     for tile in v]
                 for k, v in tiles.items()}

board = {(l, c) for l in range(HEIGHT) for c in range(WIDTH)}

solutions = find_solutions(numeric_tiles, board)
print(len(solutions))

print('\n'.join([' '.join([k for c in range(WIDTH)
                           for k, v in solutions[0].items() if (c, l) in v])
                 for l in range(HEIGHT)]))
