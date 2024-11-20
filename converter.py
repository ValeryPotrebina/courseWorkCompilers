import math
import random
from model import BinaryOpNode, FunctionNode, NumberNode, VariableNode, UnaryOpNode


def generate_random_numbers(num_variables, min_value=1, max_value=3):
    return [random.randint(min_value, max_value) for _ in range(num_variables)]


def colectVariables(node):
    if isinstance(node, NumberNode):
        return []
    if isinstance(node, VariableNode):
        return [node.name]
    if isinstance(node, FunctionNode):
        return colectVariables(node.arg)
    if isinstance(node, BinaryOpNode):
        return list(set(colectVariables(node.left) + colectVariables(node.right)))
    if isinstance(node, UnaryOpNode):
        return colectVariables(node.operand)
    return []


def convert(node):
    vars = sorted(colectVariables(node))
    return vars, convertNode(node, vars)

def convertNode(node, vars):
    if isinstance(node, NumberNode):
        return lambda args: node.value
    if isinstance(node, VariableNode):
        return lambda args: args[vars.index(node.name)]
    if isinstance(node, BinaryOpNode):
        if node.operator == '+':
            return lambda args: convertNode(node.left, vars)(args) + convertNode(node.right, vars)(args)
        if node.operator == '-':
            return lambda args: convertNode(node.left, vars)(args) - convertNode(node.right, vars)(args)
        if node.operator == '*':
            return lambda args: convertNode(node.left, vars)(args) * convertNode(node.right, vars)(args)
        if node.operator == '/':
            return lambda args: convertNode(node.left, vars)(args) / convertNode(node.right, vars)(args)
        if node.operator == '^':
            return lambda args: convertNode(node.left, vars)(args) ** convertNode(node.right, vars)(args)
    if isinstance(node, UnaryOpNode):
        if node.operator == '-':
            return lambda args: -convertNode(node.operand, vars)(args)
        if node.operator == '+':
            return lambda args: convertNode(node.operand, vars)(args)
    if isinstance(node, FunctionNode):
        if node.name == 'sin':
            return lambda args: math.sin(convertNode(node.arg, vars)(args))
        if node.name == 'cos':
            return lambda args: math.cos(convertNode(node.arg, vars)(args))
        if node.name == 'tg':
            return lambda args: math.tan(convertNode(node.arg, vars)(args))
        if node.name == 'ctg':
            return lambda args: 1 / math.tan(convertNode(node.arg, vars)(args))
        if node.name == 'asin':
            return lambda args: math.asin(convertNode(node.arg, vars)(args))
        if node.name == 'acos':
            return lambda args: math.acos(convertNode(node.arg, vars)(args))
        if node.name == 'atg':
            return lambda args: math.atan(convertNode(node.arg, vars)(args))
        if node.name == 'actg':
            return lambda args: (math.pi / 2) -math.atan(convertNode(node.arg, vars)(args))
        if node.name == 'ln':
            return lambda args: math.log(convertNode(node.arg, vars)(args))
        if node.name == 'lg':
            return lambda args: math.log10(convertNode(node.arg, vars)(args))
    return lambda args: None
