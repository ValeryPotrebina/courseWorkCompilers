from model import NumberNode, VariableNode, BinaryOpNode, FunctionNode, UnaryOpNode
import math
from simplify.simplify import simplify

def getArgs(node):
    if (isinstance(node, NumberNode)):
        return []
    if (isinstance(node, VariableNode)):
        return [node.name]
    if (isinstance(node, FunctionNode)):
        return getArgs(node.arg)
    if (isinstance(node, BinaryOpNode)):
        return list(set(getArgs(node.left) + getArgs(node.right)))
    if (isinstance(node, UnaryOpNode)):
        return getArgs(node.operand)

def calcExpr(node):
    if (isinstance(node, NumberNode)):
        return node.value
    if (isinstance(node, BinaryOpNode)):
        left = calcExpr(node.left)
        right = calcExpr(node.right)
        if (node.operator == "+"):
            return left + right
        if (node.operator == "-"):
            return left - right
        if (node.operator == "*"):
            return left * right
        if (node.operator == "/"):
            return left / right
        if (node.operator == "^"):
            return math.pow(left, right)
        if (node.operator == "="):
            return left == right
        if (node.operator == ">="):
            return left >= right
        if (node.operator == "<="):
            return left <= right
        if (node.operator == ">"):
            return left > right
        if (node.operator == "<"):
            return left < right
    if (isinstance(node, FunctionNode)):
        arg = calcExpr(node.arg)
        if (node.name) == "sin":
            return math.sin(arg)
        if (node.name) == "cos":
            return math.cos(arg)
        if (node.name) == "tg":
            return math.tan(arg)
        if (node.name) == "ctg":
            return 1 / math.tan(arg)
        if (node.name) == "asin":
            return math.asin(arg)
        if (node.name) == "acos":
            return math.acos(arg)
        if (node.name) == "atg":
            return math.atan(arg)
        if (node.name) == "actg":
            return (math.pi / 2) - math.atan(arg)
        if (node.name) == "ln":
            return math.log(arg)
        if (node.name) == "lg":
            return math.log10(arg)
        
        # Добавить в основание в log
    if (isinstance(node, UnaryOpNode)):
        value = calcExpr(node.operand)
        if (node.operator == "+"):
            return value
        if (node.operator == "-"):
            return -value


def calcComparison(node):
    # x + 5 = 2
    comparisonBody = BinaryOpNode(node.left, '-', node.right)
    operator = node.operator
    # comparisonBody = x + 5 - (2)
    # operator = "="
    # x + 5 - (2) = 0

    # comparisonBody operator 0
    return 



    




def calc(node):
    return simplify(node)




def isFunction(node):
    if (isinstance(node, BinaryOpNode) and node.operator == "=" and isinstance(node.left, VariableNode)):
        return True
    return False

def isComparison(node):
    if (isinstance(node, BinaryOpNode) and (node.operator in ['=', '>=', '<=', '>', '<'])):
        return True
    return False



# 5 + x = 