from .solve import solve
from .graph import graph
def analyze(f, f_letter,  vars):
    # print(f, vars)
    if (f_letter is None and len(vars) == 0):
        return [], []
    if (f_letter is not None and len(vars) == 0): 
        points = graph(f, 1, -6, 6, 300)
        return [], points
    roots = solve(f, vars)
    points = graph(f, len(vars), -6, 6, 300)
    print(points)
    return roots, points


# y - x   -> z = y - x  (График + решение) 3мер
# y - x = 0 -> y = x (График + решение) 2мер
# f(x) =




 
        

    # function string
    # root
    # graph points
    # projection 





