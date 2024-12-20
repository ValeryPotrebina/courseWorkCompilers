from matplotlib import pyplot as plt
import numpy as np

# class Point:
#     def __init__(self, point, value):
#         self.point = point
#         self.value = value

def graph(f, vars_count, min=-1, max=1, n=1000):
    if (vars_count != 1 and vars_count != 2):
        return None
    points = generate_points(vars_count, max, min, n)
    
    # [[x, y, z], ///]
    return [point + [f(point)] for point in points]

    

def generate_points(vars_count, min=-1, max=1, n=1000):
    
    arg_values = np.linspace(min, max, n)

    # [[1], 2, 3, 4, 5, 6]

    if vars_count == 1:
        # [[1], [2], 3, 4, 5, 6]
        return [[x] for x in arg_values]
    if vars_count == 2:
        # [[1, 2], [2, 3], 3, 4, 5, 6]
        return [[x, y] for x in arg_values for y in arg_values]
    
