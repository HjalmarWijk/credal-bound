def lower_bound(nodes, indicators, Const, log=False, ubound=float('inf'), max_steps=10):
    projection = [node.eval(indicators, log=log, solve_once=True) for node in nodes]
    old_best = -1
    new_best = projection[-1]
    print('First guess is ', new_best)
    for var in Const:
        for constset in var.values():
            print(constset.name, constset.sol)
    i = 0
    while old_best < new_best < ubound and i < max_steps:
        old_best = new_best
        for var in Const:
            for constraint in var.values():
                i += 1
                if i >= max_steps:
                    break

                def solve_with_vert(vert):
                    constraint.set_vertex(vert)
                    new = [node.eval(indicators, log=log, solve_once=True) for node in nodes]
                    return new[-1]

                best_vert = max([(vert, solve_with_vert(vert)) for vert in constraint.vertices], key=lambda k: k[1])
                constraint.set_vertex(best_vert[0])
                new_best = best_vert[1]
    return new_best
