from math import isnan
from matplotlib import pyplot as plt
import numpy as np

# class Point:
#     def __init__(self, point, value):
#         self.point = point
#         self.value = value

def graph(f, vars_count, min=-1, max=1, n=1000):
    if vars_count == 0:
        return private_solution(f, min, max, n)
    if (vars_count != 1 and vars_count != 2):
        return None
    
    points = generate_points(vars_count, max, min, n)
    
    return [point + [calc(f, point)] for point in points]


def private_solution(f, min=-1, max=1, n=1000):
    # Извлекаем значение x из функции f
    arg_values = np.linspace(min, max, n)
    x_value = [[f(x)] for x in arg_values]
    # Генерируем значения y от min до max
    y_values = [[y] for y in arg_values]
    # Создаем массив точек, где x всегда равен x_value
    points = [[x_value, y_values]]
    return points

def calc(f, point):
    res = None
    try:
        res = f(point)
    except:
        pass
    return res
    

def generate_points(vars_count, min=-1, max=1, n=1000):
    
    arg_values = np.linspace(min, max, n)
    # [[1], 2, 3, 4, 5, 6]
    if vars_count == 1:
        # [[1], [2], 3, 4, 5, 6]
        return [[x] for x in arg_values]
    if vars_count == 2:
        # [[1, 2], [2, 3], 3, 4, 5, 6]
        return [[x, y] for x in arg_values for y in arg_values]
    
    
