#!/usr/bin/python3

def read(filename):
    with open(filename, 'r') as file:
        lines = [l for l in file.readlines() if not l.isspace() ]
        nv = int(lines[1].split()[0])
        v = [tuple(float(x) for x in l.split())   for l in lines[2:nv+2] ]
        f = [tuple(int(x) for x in l.split()[1:]) for l in lines[nv+2:]  ]
    return v, f


def write(filename, v, f):
    with open(filename, 'w') as file:
        file.write('OFF\n')
        file.write(f'{len(v)} {len(f)} 0\n')
        for vstring in v:
            file.write(f'{vstring}\n')
        for fstring in f:
            file.write(f'{fstring}\n')
