from time import asctime

WIDTH = 11
HEIGHT = 5


def find_solutions(tiles, free, so_far=None):
    so_far = {} if not so_far else so_far
    if not free:
        return [so_far]
    solutions = []
    # Find all possile placements for the next tile
    for placed in filter(lambda x: all([p in free for p in x[1]]),
                         [(key, [[sum(x) for x in zip(p, free[0])] for p in t])
                          for key, tile in tiles.items() if key not in so_far
                          for t in tile]):
        solutions += find_solutions(tiles,
                                   [p for p in free if p not in placed[1]],
                                   {**{placed[0]: placed[1]}, **so_far})
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

numeric_tiles = {k: [sorted([[line[0], char[0] - tile.splitlines()[0].index(k)]
                             for line in enumerate(tile.splitlines())
                             for char in enumerate(line[1]) if char[1] != ' '])
                     for tile in v]
                 for k, v in tiles.items()}

board = sorted([[l, c] for l in range(HEIGHT) for c in range(WIDTH)])
print(asctime())
solutions = find_solutions(numeric_tiles, board)
print(asctime())
print(len(solutions))

# for s in solutions:
#     print('=====')
#     print('\n'.join([' '.join([k for c in range(WIDTH) for k,v in s.items() if [l, c] in v]) for l in range(HEIGHT)]))
	