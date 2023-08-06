#!/usr/bin/python3

def read(filename):
    with open(filename, 'r') as file:
        lines = [l for l in file.readlines() if not l.isspace() ]
        nv = int(lines[1].split()[0])
        v = [tuple(float(x) for x in l.split())   for l in lines[2:nv+2] ]
        f = [tuple(int(x) for x in l.split()[1:]) for l in lines[nv+2:]  ]
    return v, f


def write(filename, m, print_vertex=lambda v: f'{v.x} {v.y} {v.z}'):
    with open(filename, 'w') as file:
        file.write('OFF\n')
        file.write(f'{m.number_of_vertices()} {m.number_of_faces()} 0\n')
        for v in m.vertices():
            file.write(print_vertex(v) + '\n')
        for f in m.faces():
            file.write(f'3 {f[0]} {f[1]} {f[2]}\n')
