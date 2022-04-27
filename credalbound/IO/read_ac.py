class ACentry:
    def __init__(self, ac_string):
        self.node_type = None
        if ac_string[0] == 'L':
            self.id_num = int(ac_string[1])
            self.node_type = 'L'
        if ac_string[0] == 'A':
            self.child_ids = [int(i) for i in line[2:]]
            self.node_type = 'A'
        if ac_string[0] == 'O':
            self.ind_id = int(ac_string[1])
            self.child_ids = [int(i) for i in line[3:]]
            self.node_type = 'O'


class ACReader:
    def __init__(self, reader):
        self.reader = reader
        line = self.get_stripped()
        self.linenum = int(line[1])

    def next_entry(self):
        line = self.get_stripped()
        if not line:
            return None
        else:
            return ACentry(line)

    def get_stripped(self):
        line = self.reader.readline()
        if not line:
            return None
        else:
            return line.strip().split()
