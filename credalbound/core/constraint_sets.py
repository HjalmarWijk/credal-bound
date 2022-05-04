class ConstraintSet():
    def __init__(self, domsize, name):
        self.log = False
        self.solves = 0
        self.name = name
        self.domsize = domsize
        self.sol = None

    def solve(self, weights, log=0, get_sol=False):
        pass

    def value_at_vertex(self, vert, weights):
        return sum([pair[0] * pair[1] for pair in zip(weights, vert)])

    def solve_once(self, weights, log=0):
        if not self.sol:
            self.sol = self.solve(weights, get_sol=True, log=log)
        return self.value_at_vertex(self.sol, weights)


class VConstraintSet(ConstraintSet):
    def __init__(self, domsize, name, vertices=None):
        if vertices:
            self.vertices = vertices
        else:
            self.vertices = []
        super().__init__(domsize, name)
        self.sol_index = None

    def add_vertex(self, vertex):
        self.vertices.append(vertex)

    def config_vertex(self, index, value, prob):
        if len(self.vertices) <= index:
            print('Modifying non-existent vertex')
            return False
        else:
            self.vertices[index][value] = prob

    def value_at_index(self, index, weights):
        return self.value_at_vertex(self.vertices[index], weights)

    def solve(self, weights, log=0, get_sol=False):
        if not get_sol:
            return max([self.value_at_vertex(vert, weights) for vert in self.vertices])
        else:
            return max(self.vertices, key=lambda vertex: self.value_at_vertex(vertex, weights))

    def set_vertex(self, vertex):
        assert vertex in self.vertices
        self.sol = vertex
