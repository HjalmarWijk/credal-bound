class Lmapentry:
    def __init__(self, lmap_string, VarToId):
        self.node_type = None
        if lmap_string[0] == 'C':
            self.id_num = int(lmap_string[1])
            self.node_type = 'C'
        if lmap_string[0] == 'I':
            self.id_num = int(lmap_string[1])
            self.var = VarToId[lmap_string[4]]
            self.value = int(lmap_string[5])
            self.node_type = 'I'
        if lmap_string[0] == 'P':
            self.id_num = int(lmap_string[1])
            self.paramvalue = float(lmap_string[2])
            self.var = VarToId[lmap_string[4]]
            self.varvalue = int(lmap_string[8])
            self.parvalues = []
            for i in range(int(lmap_string[6]) - 1):
                self.parvalues.append((VarToId[lmap_string[9 + 2 * i]],int(lmap_string[10 + 2 * i])))
            self.node_type = 'P'


class LmapReader:
    def __init__(self, reader):
        self.reader = reader
        for i in range(6):
            line = self.get_stripped()
        self.numvar = int(line[1])
        self.VarToId = {}
        self.DomSizes = [None]
        for i in range(self.numvar):
            line = self.get_stripped()
            self.VarToId[line[1]] = i
            self.DomSizes[i] = int(line[2])

    def next_entry(self):
        line = self.get_stripped()
        entry = Lmapentry(line)
        while not entry.node_type:
            line = self.get_stripped()
            if not line:
                return None
            entry = Lmapentry(line)
        return entry

    def get_stripped(self):
        line = self.reader.readline()
        if not line:
            return None
        else:
            return line.strip().split('$')[1:]
