scoresheets = '''X -/ X 5- 8/ 9- X 81 1- 4/X
62 71  X 9- 8/  X  X 35 72 5/8
X  X  X  X  X  X  X  X  X  XXX'''

SCORES = {'X': 10, '/': 10, '-': 0}
for n in range(10):
    SCORES[str(n)] = n

for sheet in scoresheets.splitlines():
    strike, spare = 0, 0
    lastframe = sheet.split()[-1]
    print(lastframe)
    sheet = ''.join(sheet.split())
    if lastframe[1] == 'X':
        strike = SCORES['X'] + SCORES[lastframe[2]]
        spare = SCORES['X']
        sheet = sheet[:-2]
    elif lastframe[1] == '/':
        strike = 0
        spare = SCORES[lastframe[2]]
        sheet = sheet[:-1]
    score, ignore = 0, False
    for mark in sheet[::-1]:
        if not ignore:
            score += SCORES[mark]
        ignore = False
        if mark == 'X':
            score += strike
        elif mark == '/':
            score += spare
            ignore = True
        strike = spare + SCORES[mark]
        spare = SCORES[mark]
    print(score)
