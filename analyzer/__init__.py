from .solve import solve
from .graph import graph
def analyze(f, vars):
    roots = solve(f, vars)
    points = graph(f, len(vars), -10, 10, 100)
    # print(points)
    return roots, points


# y - x   -> z = y - x  (График + решение) 3мер
# y - x = 0 -> y = x (График + решение) 2мер
# f(x) =




 
        

    # function string
    # root
    # graph points
    # projection 





