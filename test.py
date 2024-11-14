from model import NumberNode, VariableNode, BinaryOpNode, FunctionNode, UnaryOpNode
from simplify.simplify import getLeftOperands, sortAddOperands

if __name__=="__main__":
    key0 = VariableNode("x")
    key1 = BinaryOpNode(VariableNode("x"), "^", NumberNode(2))
    key2 = BinaryOpNode(VariableNode("x"), "^", NumberNode(3))
    key5 = BinaryOpNode(VariableNode("x"), "^", NumberNode(-1))
    key3 = BinaryOpNode(FunctionNode("sin", VariableNode("x")), "^", NumberNode(3))
    key4 = BinaryOpNode("x", "^", "y")
    vars = [key1, key2, key3, key4, key0, key5]

    
    print(sortAddOperands(vars))

# 2 * x  -> Lest = numberNode right = node
# vars {var(x) [2]}
# 2 * Binary(x * y)
# vars {Binary(x * y), }[2]
# (2 * x) * y