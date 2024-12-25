from .solve import solve
from .graph import graph
def analyze(f, f_letter,  vars):
    if (f_letter is None and len(vars) == 0):
        return [], []
    if (f_letter is not None and len(vars) == 0): 
        points = graph(f, 1, -6, 6, 300)
        return [], points
    roots = solve(f, vars)
    points = graph(f, len(vars), -6, 6, 300)
    return roots, points