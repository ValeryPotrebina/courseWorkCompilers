from random import uniform

def quadratize(f):
    return lambda args: f(args)**2

def generate_points(n, min_value=-100, max_value=100):
    return [uniform(min_value, max_value) for _ in range(n)]

def check_root(f, x, tol=1e-6):
    return abs(f(x)) < tol
