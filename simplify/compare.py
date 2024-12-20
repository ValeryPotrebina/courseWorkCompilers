from model import BinaryOpNode, FunctionNode, NumberNode, VariableNode, UnaryOpNode
from simplify.utils import getOperands, packOperands


def parse_equal(node):
    if (isinstance(node, BinaryOpNode)):
        if (node.operator == "="):
            left = node.left 
            right = node.right
            return BinaryOpNode(
                left, 
                "-",
                right
            )
    return node

# y = x  -> y - x = 0  
# x^2 + 2x = 0  -> y = 




def find_index(list, predicate):
    return next((i for i, v in enumerate(list) if predicate(v)), None)
