from credalbound.core import PartialInstantiation
from credalbound.core import SumNode, ProdNode, IndNode


class PseudoNode:
    def __init__(self, children, node=None, variable = None):
        if node:
            self.node = node
        else:
            self.node = None
        pinsts = [child.pinst for child in children]
        self.pinst = PartialInstantiation.Join(pinsts)
        self.children = children
        self.variable = variable

    def __str__(self):
        if self.node:
            return str(self.node) + " : " + str(self.pinst)
        else:
            return "Pseudo: " + "<" + ",".join([str(child.id_num) for child in self.children]) + ">" + ":" + str(
                self.pinst)

    def __repr__(self):
        return self.__str__()

    @property
    def child_nodes(self):
        return [child.node for child in self.children if child.node is not None]

    @property
    def partial_sumnode_children(self):
        return [child for child in self.children if child.children and not child.node]

    def extend(self):
        ex_children = []
        for child in self.children:
            if child.children and not child.node:
                ex_children.extend(child.children)
            else:
                ex_children.append(child)
        self.children = ex_children

    def attach(self, node):
        self.node = node

    def assert_branching(self):
        for i in range(len(self.children)):
            try:
                assert self.children[i].pinst.get_var_value(self.variable) == i
            except AssertionError:
                print('Incorrect Branch Ordering at node {node}. Expected {exp}, instead got {res}'.format(
                    node=str(self), exp=i, res=self.children[i].pinst.get_var_value(self.variable)))


class NodeConstructor():
    def __init__(self, constmap, parmap, domsizes):
        self.Constmap = constmap
        self.curr_id = 0
        self.pnodes = []
        self.ParMap = parmap
        self.DomSizes = domsizes
        self.real_nodes = []

    def next_id(self):
        self.curr_id += 1
        return self.curr_id

    def build_sum_node(self, variable, children):
        pseudonode = PseudoNode(children)
        pseudonode.extend()
        child_nodes = pseudonode.child_nodes
        if len(child_nodes) < self.DomSizes[variable]:
            return pseudonode
        try:
            par_values = [pseudonode.pinst.get_var_value(i) for i in self.ParMap[variable]]
        except IndexError:
            print('Could not resolve parent values when creating sum node {} for variable {}, named {}'.format(
                self.next_id(), variable, pseudonode))
            for child in child_nodes:
                child.print_tree()
            raise
        constraints = self.Constmap[variable][tuple(par_values)]
        try:
            child_nodes.sort(key=lambda child: child.pinst.get_var_value(variable))
        except IndexError:
            for child in child_nodes:
                child.print_tree()
            raise
        pseudonode.assert_branching()
        node = SumNode(self.next_id(), child_nodes, constraints)
        self.real_nodes.append(node)
        pseudonode.attach(node)
        return pseudonode

    def build_prod_node(self, children):
        pnode = PseudoNode(children)
        partial_sumnodes = pnode.partial_sumnode_children
        if partial_sumnodes:
            partial_sumnodes.sort(key=lambda p: p.variable)
            to_dist = partial_sumnodes[0]
            children.remove(to_dist)
            branches = to_dist.children
            prod_list = []
            for branch in branches:
                prod_list.append(self.build_prod_node([branch]+children))
            return self.build_sum_node(to_dist.variable, prod_list)
        else:
            node = ProdNode(self.next_id(), pnode.child_nodes)
            self.real_nodes.append(node)
            pnode.attach(node)
            return pnode

    def build_ind_node(self, variable, value):
        node = IndNode(self.next_id(), variable, value)
        self.real_nodes.append(node)
        pnode = PseudoNode([], node)
        pnode.pinst.add_observation(variable, value)
        return pnode

    def build_param_node(self, par_pairs):
        pnode = PseudoNode([])
        for pair in par_pairs:
            pnode.pinst.add_observation(pair[0], pair[1])
        return pnode
