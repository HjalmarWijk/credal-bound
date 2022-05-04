import argparse

parser = argparse.ArgumentParser(description='UAI to HUGIN (.net) converter')

parser.add_argument("-u", "--uai", help="UAI file name", default="model.uai")

parser.add_argument("-o", "--outdir", default = "uai_gen")

args = parser.parse_args()

filename = args.uai
out_dir = args.outdir
outfile = out_dir+"/model.net"
oddfile = out_dir+"/fake.odd"
def node_str(name, states):
    states = ' '.join(['\"' + statename + '\"' for statename in states])
    stateline = '  states = ( {} );'.format(states)
    return 'node {0}\n{{\n{1}\n}}'.format(name,stateline)
def prob_str(n):
    return '('+ ' {:.5f}'.format(1/float(n))*n + ' )'
def conditional_prob_str(n,pardims):
    if not pardims:
        return prob_str(n)
    else:
        return '('+ conditional_prob_str(n,pardims[1:])*pardims[0] + ')'
def potential_str(var, dims, parents, pardims):
    potentials = conditional_prob_str(dims,pardims)
    potentialstr = '  data = {} ;'.format(potentials)
    parnamestring = ' '.join(['Var'+str(i) for i in parents])
    headerstring = '( Var' + str(var) + ' | ' + parnamestring + ' )'
    return 'potential {0}\n{{\n{1}\n}}'.format(headerstring,potentialstr)
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
with open(outfile, 'w') as net_file:
    net_file.write('net\n{\n}\n')
    for i in range(numvar):
        net_file.write(node_str('Var'+str(i),['State'+str(j) for j in range(domsizes[i])])+'\n')
    for i in range(numvar):
        net_file.write(potential_str(i,domsizes[i],parents[i],[domsizes[p] for p in parents[i]])+'\n')
with open(oddfile, 'w') as odd_file:
    odd_file.write('[Var0]\n')
    odd_file.write('0 0' + ' S0'*domsizes[0])

