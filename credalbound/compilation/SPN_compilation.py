import math

from credalbound.compilation import NodeConstructor
from credalbound.IO import LmapReader, ACReader, get_constmap, read_uai_verts


def load_lmap(reader: LmapReader, node_constructor: NodeConstructor):
    literals = [None] * (reader.numnodes+1)
    while entry := reader.next_entry():
        if entry.node_type == 'C':
            pass
        if entry.node_type == 'I':
            literals[entry.id_num] = node_constructor.build_ind_node(entry.var, entry.value)
        if entry.node_type == 'P':
            literals[entry.id_num] = node_constructor.build_param_node(entry.parvalues)
    #print(literals)
    return literals


def load_ac(reader: ACReader, node_constructor: NodeConstructor, literals, log = False):
    pseudonodes = [None] * reader.linenum
    i = 0
    while entry := reader.next_entry():
        if i % math.floor(reader.linenum / 100 + 1) == 0 and log:
            print('Reading AC, ', math.floor(i * 100 / reader.linenum), ' %')
        if entry.node_type == 'L' and entry.id_num > 0:
            pseudonodes[i] = literals[entry.id_num]
        if entry.node_type == 'A':
            children = [pseudonodes[child_id] for child_id in entry.child_ids]
            pseudonodes[i] = node_constructor.build_prod_node(children)
        if entry.node_type == 'O':
            children = [pseudonodes[child_id] for child_id in entry.child_ids]
            var = literals[entry.ind_id].node.variable
            pseudonodes[i] = node_constructor.build_sum_node(var, children)
        #print(i, pseudonodes[i])
        i += 1
    return pseudonodes


def compile_SPN(uai_file, lmap_file, ac_file, log = True):
    with open(lmap_file, 'r') as lmap, open(ac_file, 'r') as ac:
        domsizes, parents, vertices = read_uai_verts(uai_file)
        constmap = get_constmap(vertices)
        #print(constmap)
        lmap_reader = LmapReader(lmap)

        node_constructor = NodeConstructor(constmap, parents, domsizes)
        literals = load_lmap(lmap_reader, node_constructor)
        ac_reader = ACReader(ac)
        load_ac(ac_reader, node_constructor, literals, log = log)
        nodes = node_constructor.real_nodes
        return nodes
