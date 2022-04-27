import math


class NodeConfig:
    def __init__(self, freeze_constraints=False, log=False):
        self.freeze_constraints = freeze_constraints
        self.log = log


class Node:
    def __init__(self, id_num):
        self.stored = None
        self.par = False
        self.children = None
        self.id_num = id_num

    def init_config(self, config):
        config.par = not self.par

    def eval_query(self, query, config=None):
        if not config:
            config = NodeConfig()
        if query.conditional:
            intersection = self.eval(query.get_intersect(), config)
            conditional = self.eval(query.get_conditional(), config)

    def reset(self):
        self.par = False
        for child in self.children:
            child.reset()

    def eval(self, indicators, config=None):
        if not config:
            config = NodeConfig()
        self.init_config(config)
        return __eval__(indicators, config)

    def __eval__(self, indicators, config):
        if config.par != self.par:
            self.stored = self.computeEval(indicators, config)
            self.par = config.par
        return self.stored

    def computeEval(self, indicators, config):
        pass

    def __str__(self):
        return "[ID:{id_num}]{unique_str}".format(id_num=self.id_num, unique_str=self.unique_str())

    def __repr__(self):
        return self.__str__()

    def print_tree(self):
        print(self)
        for child in self.children:
            child.print_tree()

    def unique_str(self):
        return ""


class InnerNode(Node):
    def __init__(self, id_num, children):
        assert children
        super().__init__(id_num)
        self.children = children

    def unique_str(self):
        return "<" + ",".join([str(child.id_num) for child in self.children]) + ">"


class ProdNode(InnerNode):
    def unique_str(self):
        return "A " + super().unique_str()

    def computeEval(self, indicators, config):
        prod = math.prod(child.__eval__(indicators, config) for child in self.children)
        if config.log:
            print(
                'Prod-node with {numchild} children: {val}'.format(val=prod, numchild=len(self.children)))
        return prod


class SumNode(InnerNode):
    def unique_str(self):
        return "S:" + self.constraints.name + super().unique_str()

    def __init__(self, id_num, children, constraints):
        self.constraints = constraints
        super().__init__(id_num, children)

    def computeEval(self, indicators, config):
        if not config.freeze_constraints:
            value = self.constraints.solve([child.eval(indicators) for child in self.children], config)
        else:
            value = self.constraints.solve_once([child.eval(indicators) for child in self.children], config)
        if config.log:
            print(
                "Sum-Node {constraint}: {val} ".format(constraint=self.constraints.name, val=value))
        return value


class IndNode(Node):
    def unique_str(self):
        return "I:" + str(self.variable) + ":" + str(self.value)

    def __init__(self, id_num, variable, value):
        self.variable = variable
        self.value = value
        super().__init__(id_num)

    def computeEval(self, indicators, config):
        if indicators[self.variable] == self.value or indicators[self.variable] is None:
            if config.log:
                print('Indicator for {var} being {val}: {assigned}'.format(
                    var=self.variable, val=self.value, assigned=1))
            return 1
        else:
            if config.log:
                print('Indicator for {var} being {val}: {assigned}'.format(
                    var=self.variable, val=self.value, assigned=0))
            return 0
