scoresheets = '''X -/ X 5- 8/ 9- X 81 1- 4/X
62 71  X 9- 8/  X  X 35 72 5/8
X  X  X  X  X  X  X  X  X  XXX'''

SPECIAL = {'X', '/', '-'}
VALID = set(str(range(10))) | SPECIAL
VALID_2 = VALID - {'X'}
VALID_1 = VALID_2 - {'/'}


def is_sheet_valid(sheet):
    frames = sheet.split()
    print(frames)
    assert(len(frames) == 10)
    for frame in frames[:-1]:
        assert(set(sheet).issubset(VALID))
        if frame[-1] == 'X':
            assert(len(frame) == 1)
        else:
            assert(len(frame) == 2)
            assert(frame[0] in VALID_1 and frame[1] in VALID_2)

    last = frames[-1]
    assert(frame[0] != '/')
    if len(last) == 2:
        assert(frame[0] in VALID_1 and frame[1] in VALID_1)
    if len(last) == 3:
        assert(frame[0] == 'X' or frame[1] == '/')
        if frame[1] == 'X':
            assert(frame[0] == 'X')


print(list(map(lambda x: (x, is_sheet_valid(x)), scoresheets.splitlines())))