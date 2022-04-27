class PartialInstantiation():
    def __str__(self):
        return str(self.pinst)

    def __repr__(self):
        return self.__str__()

    def __init__(self, pinst=None):
        if not pinst:
            self.pinst = {}

    @classmethod
    def Join(cls, pinst_list):
        to_build = cls()
        for pinst in pinst_list:
            for key, item in pinst.items():
                to_build.add_observation(key, item)
        return to_build

    def add_observation(self, var, value):
        if var in self.pinst and self.pinst[var] != value:
            self.pinst[var] = None
        else:
            self.pinst[var] = value

    def get_var_value(self, var):
        if var not in self.pinst or self.pinst[var] == None:
            print('Underdetermined pinst access', var, self.pinst[var])
            raise IndexError
        return self.pinst[var]

    def items(self):
        return self.pinst.items()
