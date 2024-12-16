import numpy as np
from scipy.optimize import minimize

# Пример функции, корни которой мы хотим найти
def f(x, y):
    return x**2 - y**2

# Преобразуем функцию для минимизации
def g(xy):
    x, y = xy
    return f(x, y)**2

# Функция для нахождения корней с разными начальными точками
def find_roots(initial_points, tol=1e-6):
    roots = []
    for x0 in initial_points:
        res = minimize(g, x0, method='BFGS', options={'disp': False})
        print(res)
        root = np.round(res.x, 4)
        if not any(np.allclose(root, r, atol=tol) for r in roots):
            roots.append(root)
    return roots

# Начальные точки для оптимизации
initial_points = [
    np.array([1.0, 1.0]),
    np.array([-1.0, 1.0]),
    np.array([1.0, -1.0]),
    np.array([-1.0, -1.0]),
    np.array([2.0, 2.0]),
    np.array([-2.0, 2.0]),
    np.array([2.0, -2.0]),
    np.array([-2.0, -2.0]),
]

# Нахождение всех корней
roots = find_roots(initial_points)

print("Найденные корни уравнения:")
for root in roots:
    print(root)
