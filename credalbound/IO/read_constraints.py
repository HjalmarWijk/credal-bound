import math
from credalbound.core import VConstraintSet


def index_to_parvals(index, pardims):
    units = [1] * len(pardims)
    for i in range(len(pardims) - 1):
        units[i + 1] = units[i] * pardims[-(i + 1)]
    indices = [None] * len(pardims)
    rem = index
    for i in range(len(pardims)):
        indices[i] = rem // units[-(i + 1)]
        rem = rem % units[-(i + 1)]
    return indices


def index_to_parvals_reversed(index, pardims):
    units = [1] * len(pardims)
    for i in range(len(pardims) - 1):
        units[i + 1] = units[i] * pardims[i]
    indices = [None] * len(pardims)
    rem = index
    for i in reversed(range(len(pardims))):
        indices[i] = rem // units[i]
        rem = rem % units[i]
    return indices


def parse_vert_set(reader, domsize):
    num_vert = int(reader.readline().strip()) // domsize
    verts = [None] * num_vert
    for i in range(num_vert):
        verts[i] = [float(coord) for coord in reader.readline().strip().split(' ')]
    return verts


def read_uai_verts(filename):
    with open(filename, 'r') as model_file:
        line = model_file.readline()
        line = model_file.readline()
        numvar = int(line.strip())
        domsizes = [int(domsize) for domsize in model_file.readline().strip().split(' ')]
        line = model_file.readline()
        parents = [None] * numvar
        for i in range(numvar):
            line = model_file.readline().strip().split(' ')
            var = int(line[-1])
            parents[var] = [int(par) for par in line[1:-1]]
        Verts = [{} for i in range(numvar)]
        for i in range(numvar):
            line = model_file.readline()
            pardims = [domsizes[p] for p in parents[i]]
            for j in range(math.prod(pardims)):
                Verts[i][tuple(index_to_parvals(j, pardims))] = parse_vert_set(model_file, domsizes[i])
    return parents, Verts


def get_constmap(Verts):
    return [{key: constraints_from_verts(vertices, "{}|{}".format(i, ' '.join([str(j) for j in key]))) for
             (key, vertices) in var.items()} for (i, var) in enumerate(Vert)]


def constraints_from_verts(vert_set, name):
    return VConstraintSet(len(vert_set[0]), name, vert_set)

if __name__ == "__main__":
    for i in range(12):
        print(index_to_parvals(i, [3, 4]))
    for i in range(12):
        print(index_to_parvals_reversed(i, [3, 4]))
    # n,d,p,V = read_uai_verts('model.uai')
    # print(V)
