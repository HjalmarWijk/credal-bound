import math
import numpy as np
def index_to_parvals(index, pardims):
    units = [1]*len(pardims)
    for i in range(len(pardims)-1):
        units[i+1] = units[i]*pardims[-(i+1)]
    indices = [None]*len(pardims)
    rem = index
    for i in range(len(pardims)):
        indices[i] = rem // units[-(i+1)]
        rem = rem % units[-(i+1)]
    return indices
def index_to_parvals_reversed(index, pardims):
    units = [1]*len(pardims)
    for i in range(len(pardims)-1):
        units[i+1] = units[i]*pardims[i]
    indices = [None]*len(pardims)
    rem = index
    for i in reversed(range(len(pardims))):
        indices[i] = rem //units[i]
        rem = rem % units[i]
    return indices
def parvals_to_index(par_vals, pardims):
    units = [1]*len(pardims)
    for i in range(len(pardims)-1, 0, -1):
        units[i-1] = units[i]*pardims[i]
    return sum([par_val * unit for (par_val, unit) in zip(par_vals, units)])
def index_to_parvals_insane(index, pardims):
    par_vals_reversed = index_to_parvals_reversed(index, pardims)
    new_index = parvals_to_index(par_vals_reversed, pardims)
    par_vals = index_to_parvals_reversed(new_index, pardims)
    return par_vals

def parse_vert_set(reader, domsize):
    num_vert = int(reader.readline().strip())//domsize
    verts = [None]*num_vert
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
        parents = [None]*numvar
        for i in range(numvar):
            line = model_file.readline().strip().split(' ')
            var = int(line[-1])
            parents[var] = [int(par) for par in line[1:-1]]
        Verts = [{} for i in range(numvar)]
        for i in range(numvar):
            line = model_file.readline()
            pardims = [domsizes[p] for p in parents[i]]
            for j in range(math.prod(pardims)):
                Verts[i][tuple(index_to_parvals(j,pardims))]=parse_vert_set(model_file, domsizes[i])
    return numvar, domsizes, parents, Verts


def get_dom_string(domsizes):
    s = ""
    for var in domsizes:
        s += str(var) + " "
    s += "\n"
    return s


def get_par_string(parents):
    s = ""
    for i, var in enumerate(parents):
        s += str(len(var) + 1)
        for p in var:
            s += " " + str(p)
        s += " " + str(i)
        s += "\n"
    return s

def get_cpt_string(cpt, epsilon):
    cpt = np.array(cpt)
    size = cpt.size
    dom_size = cpt.shape[-1]
    verts = (dom_size-1)*2
    num_dists = size//dom_size
    s = ""
    for i in range(num_dists):
        s += str(dom_size*verts) + "\n"
        par_tuple = index_to_parvals_insane(i, cpt.shape[:-1])
        for k in range(verts//2):
            for j in range(dom_size):
                val = cpt[tuple(par_tuple) + (j,)]
                if j == k:
                    diff = min(epsilon, 1-val)
                    val += diff
                if j == dom_size-1:
                    val -= diff
                s += f'{val:.5f}' + " "
            s += "\n"
            for j in range(dom_size):
                val = cpt[tuple(par_tuple) + (j,)]
                if j == k:
                    diff = min(epsilon, val)
                    val -= diff
                if j == dom_size - 1:
                    val += diff
                s += f'{val:.5f}' + " "
            s += "\n"
    return s


def print_uai(filename, domsizes, parents, cpt, epsilon):
    with open(filename, 'w') as uai_file:
        uai_file.write("V-CREDAL" + "\n")
        uai_file.write(str(len(domsizes)) + "\n")
        uai_file.write(get_dom_string(domsizes))
        uai_file.write(str(len(domsizes)) + "\n")
        uai_file.write(get_par_string(parents))
        for var in cpt:
            uai_file.write("\n")
            uai_file.write(get_cpt_string(var, epsilon))
if __name__ == "__main__":
    pass
    #n,d,p,V = read_uai_verts('model.uai')
    #print(V)

