from re import findall

INPUT = '''4
edcf
bnik
poil
vybu'''

def broken_kb(word):
        return max((s for s in findall(r'\b[{}]+\b'.format(keys),
                                       open('enable1.txt').read())), key=len)


for keys in INPUT.splitlines()[1:]:
    print('{} = {}'.format(keys, broken_kb(keys)))
