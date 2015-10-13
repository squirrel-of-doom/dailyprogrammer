from random import randrange
from collections import Counter


def random_bag(tiles):
    while True:
        bag = list(tiles)
        while len(bag):
            yield bag.pop(randrange(len(bag)))


def validate_output(tiles, output):
    if not len(output):
        return True
    c = Counter(output[:7])
    if (c.keys() - tiles) or any(c[t] > 1 for t in tiles):
        return False
    return validate_output(tiles, output[7:])


TILES = {'O', 'I', 'S', 'J', 'L', 'Z', 'T'}
gen = random_bag(TILES)
output = ''.join([next(gen) for _ in range(50)])
print(output)
print(validate_output(TILES, output))
print(validate_output(TILES, 'OISJLZO'))
