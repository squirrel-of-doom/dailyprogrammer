from ast import literal_eval

def primes(stop):
    yield 2
    primes = []
    for n in range(3, stop + 1, 2):
        if not primes or all([n % p for p in primes]):
            primes += [n]
            yield n

def psum(n):
    if n <= 1:
        return 0
    sum = 0
    for p in primes(n):
        r = n % p
        sum += 0 if r else p
        while not (n % p):
            n //= p
        if n == 1:
            break
    return sum

pairs = [literal_eval(l) for l in open('input.txt').read().splitlines()[1:]]
for result in [(pair, psum(pair[0]) == psum(pair[1])) for pair in pairs]:
    print('{} {}'.format(result[0], ['NOT VALID', 'VALID'][result[1]]))
