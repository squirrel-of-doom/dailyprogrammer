import re
from math import gcd


def insert(compound, name, n=1):
    if not name in compound:
        compound[name] = 0
    compound[name] += n


def get_subs(resub, resplit, molstr, mul=1):
    molecule = {}
    for match in re.finditer(resub, molstr):
        n = int(match.group(2)) if match.group(2) else 1
        insert(molecule, match.group(1), n * mul)
    for s in re.split(resplit, molstr):
        if s:
            insert(molecule, s, mul)
    return molecule


def parse_molecule(molstr):
    elem_re = re.compile('([A-Z][a-z]?)(\d)*')
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
    return molecules, elements


def get_lcm_count(element):
    lcm = 1
    for n in element.values():
        lcm = lcm * n // gcd(lcm, n)
    return lcm


def apply_total(mol, elems, el, total):
    for m, n in elems[el].items():
        mol[m] *= total // n
    for other_el in elems:
        for m in elems[other_el]:
            if m in elems[el]:
                elems[other_el][m] *= mol[m]
        

def get_coeffs_gcd(reac, prod):
    result = 0
    for coeff in reac.values():
        if not result:
            result = coeff
        result = gcd(result, coeff)
    return result
    
def make_side(mol, divisor):
    return ' + '.join([str(n // divisor) + ' ' + m for m, n in mol.items()])


def balance_equation(skeleton):
    lhs, _, rhs = skeleton.partition('->')
    reac_mol, reac_elem = parse_side(lhs)
    prod_mol, prod_elem = parse_side(rhs)
    if set(reac_elem) != set(prod_elem):
        return 'Nope!'
    for elem in set(reac_elem):
        pre_cnt = get_lcm_count(reac_elem[elem])
        post_cnt = get_lcm_count(prod_elem[elem])
        total = pre_cnt * post_cnt // gcd(pre_cnt, post_cnt)
        apply_total(reac_mol, reac_elem, elem, total)
        apply_total(prod_mol, prod_elem, elem, total)
    div = get_coeffs_gcd(reac_mol, prod_mol)
    return ' <- '.join([make_side(reac_mol, div), make_side(prod_mol, div)])
    

beq = balance_equation('Al + Fe2O4 -> Fe + Al2O3')
print(beq)
