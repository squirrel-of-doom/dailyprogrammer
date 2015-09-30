from functools import reduce
from operator import mul


def ordered_fangs(start, stop, count):
    for outer in range(start, stop):
        if count == 1:
            yield outer,
        else:
            for inner in ordered_fangs(outer, stop, count - 1):
                yield (outer,) + inner


def is_vampire(fangs):
    vampire = 1
    fang_digits = []
    for fang in fangs:
        fang_digits += str(fang)
        vampire *= fang
    return sorted(str(vampire)) == sorted(fang_digits)


S_PROMPT = 'Input number length and fang length: '
num_length, fang_num = tuple(map(int, input(S_PROMPT).split(maxsplit=1)))
fang_length = num_length // fang_num

start = 10 ** (fang_length - 1)
all_fangs = filter(is_vampire, ordered_fangs(start, 10 * start, fang_num))
vampires = [(reduce(mul, f), f) for f in all_fangs if reduce(mul, f) % 100 > 0]

for v in vampires:
    print("{} = {}".format(v[0], " * ".join(map(str, v[1]))))
