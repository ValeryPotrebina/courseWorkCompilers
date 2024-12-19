from scipy.optimize import minimize
from .utils import generate_points, quadratize, check_root
import numpy as np

def solve(f, vars, tol=1e-6, root_count=6, max_iter=1000):
    g = quadratize(f)
    roots = []
    while True:
        found = False
        for _ in range(round(max_iter)):
            x0 = generate_points(len(vars))
            res = minimize(g, x0, tol=tol, method='BFGS', options={'disp': False}, )
            if not res.success:
                continue
            x = res.x
            if not check_root(f, x, tol=tol):
                continue
            if not any(np.allclose(x, r, atol=tol) for r in roots):
                roots.append(x)
                found = True
                break
        if not found or len(roots) == root_count:
            break
    return roots



