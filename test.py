from model import NumberNode, VariableNode, BinaryOpNode, FunctionNode, UnaryOpNode
from simplify.simplify import getLeftOperands

if __name__=="__main__":
    vars = {}
    key1 = BinaryOpNode(VariableNode("x"), "*", VariableNode("y"))
    key2 = BinaryOpNode(VariableNode("x"), "*", VariableNode("y"))
    value1 = [1, 2]
    value2 = [2, 3]

if (vars.get(key1.name) is None):
    vars[key1.name] = []
vars[key1.name] += value1
 
if (vars.get(key2.name) is None):
    vars[key2.name] = []
vars[key2.name] += value2

print(vars)


print(getLeftOperands())

# 2 * x  -> Lest = numberNode right = node
# vars {var(x) [2]}
# 2 * Binary(x * y)
# vars {Binary(x * y), }[2]
# (2 * x) * y