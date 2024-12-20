from model import BinaryOpNode, FunctionNode, NumberNode, VariableNode, UnaryOpNode
from simplify.utils import getOperands, packOperands, colectVariables


def parse_equal(node):
    if (isinstance(node, BinaryOpNode)):
        if (node.operator == "="):
            left = node.left 
            right = node.right
            if (isinstance(left, VariableNode) and not find_var(right, left.name)):
                return left.name, right
            return None, BinaryOpNode(
                left, 
                "-",
                right
            )
    return None, node


def find_var(node, var):
    if isinstance(node, VariableNode):
        return node.name == var
    if isinstance(node, FunctionNode):
        return find_var(node.arg, var)
    if isinstance(node, BinaryOpNode):
        left = find_var(node.left, var)
        right = find_var(node.right, var)
        return left or right
    if isinstance(node, UnaryOpNode):
        return find_var(node.operand, var)
    return False


def find_index(list, predicate):
    return next((i for i, v in enumerate(list) if predicate(v)), None)
