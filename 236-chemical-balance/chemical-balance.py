from math import gcd
from operator import mul
import re


def insert(compound, name, n=1):
    if not name in compound:
        compound[name] = 0
    compound[name] += n


def get_subs(sub_re, split_re, molstr, mul=1):
    molecule = {}
    for match in re.finditer(sub_re, molstr):
        n = int(match.group(2)) if match.group(2) else 1
        insert(molecule, match.group(1), n * mul)
    for s in re.split(split_re, molstr):
        if s:
            insert(molecule, s, mul)
    return molecule


def parse_molecule(molstr):
    elem_re = re.compile('([A-Z][a-z]?)(\d*)')
    elements = {}
    compounds = get_subs('\[([\w\(\)]+)\](\d*)', '\[[\w\(\)]+\]\d*', molstr)
    for s0, n0 in compounds.items():
        comps = get_subs('\(([\w\(\)]+)\)(\d*)', '\([\w\(\)]+\)\d*', s0, n0)
        for s1, n1 in comps.items():
           for elem_cnt in elem_re.finditer(s1):
               n = int(elem_cnt.group(2)) if elem_cnt.group(2) else 1
               insert(elements, elem_cnt.group(1), n * n1)
    return elements


def parse_side(side):
    molecules = {m.strip(): 1 for m in side.split('+')}
    elements = {}
    for molecule in molecules:
        for element, count in parse_molecule(molecule).items():
            if not element in elements:
                elements[element] = {}
            elements[element][molecule] = count
    return {'M': molecules, 'E': elements}


def get_lcm_count(element):
    lcm = 1
    for n in element.values():
        lcm = lcm * n // gcd(lcm, n)
    return lcm


def apply_total(side, elem, total):
    print(side, elem, total)
    #  Update molecule count
    for m, n in side['E'][elem].items():
        side['M'][m] *= total // n
    #  Feedback into other elements
    for other in side['E']:
        for m in side['E'][other]:
            if m in side['E'][elem]:
                side['E'][other][m] *= side['M'][m]
    print(side)


def get_coeffs_gcd(coeffslist):
    result = 0
    for coeffs in coeffslist:
        for coeff in coeffs:
            if not result:
                result = coeff
            result = gcd(result, coeff)
    return result


def get_coeff_str(n, divisor):
    coeff = n // divisor
    if coeff > 1:
        return str(coeff)
    return ''


def make_side(mol, divisor):
    return ' + '.join([get_coeff_str(n, divisor) + m for m, n in mol.items()])


def balance_equation(skeleton):
    sides = [parse_side(sidestr) for sidestr in skeleton.split('->')]
    if set(sides[0]['E']) != set(sides[1]['E']):
        return 'Nope!'
    for elem in set(sides[0]['E']):
        elem_cnt = tuple(get_lcm_count(side['E'][elem]) for side in sides)
        total = mul(*elem_cnt) // gcd(*elem_cnt)
        for side in sides:
            apply_total(side, elem, total)
    div = get_coeffs_gcd([side['M'].values() for side in sides])
    return ' <- '.join([make_side(side['M'], div) for side in sides])
    

INPUT = '''C5H12 + O2 -> CO2 + H2O
'''
#Zn + HCl -> ZnCl2 + H2
#Ca(OH)2 + H3PO4 -> Ca3(PO4)2 + H2O
#FeCl3 + NH4OH -> Fe(OH)3 + NH4Cl
#K4[Fe(SCN)6] + K2Cr2O7 + H2SO4 -> Fe2(SO4)3 + Cr2(SO4)3 + CO2 + H2O + K2SO4 + KNO3'''

for eq in INPUT.splitlines():
    print(balance_equation(eq))
