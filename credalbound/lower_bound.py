def lower_bound(nodes, pinst, Const, full_results=False, log=False, ubound=float('inf'),max_steps = 10):
    for node in nodes:
        node.stored = None
    new = [node.eval(pinst, log=log, solve_once=True) for node in nodes]
    for node in nodes:
        node.stored = None
    old_best = -1
    new_best = new[-1]
    print('First guess is ', new_best)
    for var in Const:
        for constset in var.values():
            print(constset.name,constset.sol)
    i=0
    while new_best > old_best and new_best < ubound and i<max_steps:
        old_best = new_best
        for var in Const:
            for constraint in var.values():
                i += 1
                constraint.swap()
                new =  [node.eval(pinst, log=log, solve_once=True) for node in nodes]
                for node in nodes:
                    node.stored = None
                if new[-1] > new_best:
                    new_best = new[-1]
     #               print('Improved to ', new_best)
                else:
                    constraint.swap()
    return new_best