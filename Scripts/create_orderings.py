import random
from credalbound.IO import read_uai_verts
import argparse
parser = argparse.ArgumentParser(description='Create all possible orderings compatible with uai file')
parser.add_argument("-i","--input")
parser.add_argument("-o","--out_dir",default='orders')
parser.add_argument("-l","--limit",default=100)
args = parser.parse_args()

def all_possible_orderings(parents, cap = 100):
    var_list = list(range(len(parents)))
    orderings = [[]]
    for i in range(len(parents)):
        new_orderings = []
        for order in orderings:
            if len(new_orderings) == cap:
                break
            possible = [var for var in var_list if var not in order and all(par in order for par in parents[var])]
            random.shuffle(possible)
            for var in possible:
                new_orderings.append(order+[var])
                if len(new_orderings)==cap:
                    break
        orderings = new_orderings
    return orderings
#print(len(all_possible_orderings([[],[0,2],[],[1,4],[],[3],[2],[],[5]])))
def print_ordering(filename,ordering):
    with open(filename,'w') as f:
        for i, var in enumerate(ordering):
            parstr = ' '.join(['Var'+str(p) for p in ordering[:i]])
            f.write('Var'+str(var) + ' ' + parstr + '\n')
filename = args.input
_,parents,_ = read_uai_verts(filename)
for i, order in enumerate(all_possible_orderings(parents,cap=int(args.limit))):
    print_ordering(args.out_dir +'/order' + str(i)+'.txt', order)
    
