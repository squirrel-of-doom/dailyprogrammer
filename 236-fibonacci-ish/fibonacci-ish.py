from timeit import timeit


def fibonacci(stop):
    f1, f2, fib = 0, 0, 1
    while fib <= stop:
        yield fib
        f1, f2 = f2, fib
        fib = f1 + f2


def fib_ish(n):
    fibs, seeds = [0], [(n, 1)]
    for idx, f in enumerate(fibonacci(n)):
        fibs.append(f)
        q, rem = divmod(n, f)
        if not rem:
            seeds.append((q, idx + 2))  # 1 for offset sequence, 1 for slicing
    seed, stop = min(seeds)
    return [seed * f for f in fibs[:stop]]


print(fib_ish(0))
print(fib_ish(578))
print(fib_ish(123456789))
print(fib_ish(38695577906193299))

setup_stmt = 'from __main__ import fib_ish'
print(timeit('fib_ish(0)', setup=setup_stmt) / 1000, 'ms')
print(timeit('fib_ish(578)', setup=setup_stmt) / 1000, 'ms')
print(timeit('fib_ish(123456789)', setup=setup_stmt) / 1000, 'ms')
print(timeit('fib_ish(38695577906193299)', setup=setup_stmt) / 1000, 'ms')
