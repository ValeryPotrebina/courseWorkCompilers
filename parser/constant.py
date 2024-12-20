import math
from model import NumberNode, VariableNode, FunctionNode, BinaryOpNode, UnaryOpNode, ConstantNode, CONSTANTS


def define_constant(node):
    if isinstance(node, VariableNode):
        if (node.name in CONSTANTS):
            return ConstantNode(node.name)
    if isinstance(node, FunctionNode):
        return FunctionNode(node.name, define_constant(node.arg))
    if isinstance(node, BinaryOpNode):
        return BinaryOpNode(define_constant(node.left), node.operator, define_constant(node.right))
    if isinstance(node, UnaryOpNode):
        return UnaryOpNode(define_constant(node.operand))
    return node



