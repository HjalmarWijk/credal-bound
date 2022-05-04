from credalbound.IO.uai import print_uai


class NetReader:

    def __init__(self, reader):
        self.reader = reader
        for i in range(3):
            self.read_line()

    def read_line(self, floats=False):
        line = self.reader.readline().strip()
        if not line:
            return None
        line = line.replace('|', '').replace('=', '').replace(';', '')
        if '(' in line:
            line = line.split('(', 1)
            line[1] = self.parse_parenthesis_block(line[1][:-1].strip(), floats=floats)
            line[0] = line[0].strip()
        else:
            line = line.strip().split()
        return line

    @staticmethod
    def parse_parenthesis_block(string, floats=False):
        if string[0] != '(':
            split = string.split()
            if floats:
                split = [float(x) for x in split]
            return split
        start_index = 0
        spare_left_pars = 0
        blocks = []
        for i in range(len(string)):
            if string[i] == '(':
                spare_left_pars += 1
            if string[i] == ')':
                spare_left_pars -= 1
            if spare_left_pars == 0:
                print('Splitting off block', string[start_index:i + 1])
                blocks.append(NetReader.parse_parenthesis_block(string[start_index + 1:i], floats=floats))
                start_index = i + 1
        return blocks

    def read_block(self):
        line = self.read_line()
        if not line:
            return None
        block_type = line[0]
        identifier = line[1]
        self.read_line()
        floats = block_type == 'potential'
        line = self.read_line(floats=floats)
        data = line[1]
        self.read_line()
        return block_type, identifier, data


def load_net_file(filename):
    with open(filename, 'r') as file:
        reader = NetReader(file)
        varnames = []
        domsizes = []
        block_info = reader.read_block()
        while block_info[0] == 'node':
            varnames.append(block_info[1])
            domsizes.append(len(block_info[2]))
            print('Read var ', block_info[1])
            block_info = reader.read_block()
        parents = [None] * len(varnames)
        cpt = [None] * len(varnames)
        print('Reading potentials')
        while block_info:
            var_id = varnames.index(block_info[1][0])
            pars = [varnames.index(p) for p in block_info[1][1:]]
            parents[var_id] = pars
            print('Read potential for ', block_info[1][0])
            cpt[var_id] = block_info[2]
            block_info = reader.read_block()
    return domsizes, parents, cpt
