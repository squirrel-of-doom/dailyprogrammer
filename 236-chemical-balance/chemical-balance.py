import re

OPEN_BLOCK = {'(', '[', '{'}
CLOSE_BLOCK = {'(': ')', '[': ']', '{': '}'}


def create_node(name, n=1):
    return {'MOL': name, 'N': n, 'SUB': []}


def parse_molecule(molstr):
    print(molstr)
    molecule = create_node(molstr)
    element, count = '', 0
    for char in molstr:
        if char.isdigit():
            count = count * 10 + int(char)
        elif char.isupper():
            if element:
                count = count or 1
                molecule['SUB'].append(create_node(element, count))
            element, count = char, 0
        elif char.islower:
            element += char
    count = count or 1
    if element != molstr:
        molecule['SUB'].append(create_node(element, count))
    print(molecule)
    return molecule


def balance_equation(skeleton):
    lhs, _, rhs = skeleton.partition('->')
    reactants = [parse_molecule(s.strip()) for s in lhs.split('+')]
    products = [parse_molecule(s.strip()) for s in rhs.split('+')]


balance_equation('Al + Fe2O4 -> Fe + Al2O3')