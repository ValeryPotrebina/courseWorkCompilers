from model import BinaryOpNode, FunctionNode, NumberNode, VariableNode, UnaryOpNode


# TODO getOperands - получаем массив всех операндов математического выражения
# например [VariableNode(x), VariableNode(y), BinaryOpNode(VariableNode(x), ^, NumberNode(2.0)), BinaryOpNode(VariableNode(y), ^, NumberNode(2.0))]
def getOperands(node, operator):
    if (isinstance(node, BinaryOpNode) and node.operator == operator):
        return getOperands(node.left, operator) + getOperands(node.right, operator)
    return [node]

def getLeftOperands(node, op):
    if (isinstance(node, BinaryOpNode) and node.operator == op):
        return getLeftOperands(node.left, op) + [node.right]
    return [node]

def packOperands(operands, operator):
    if (len(operands) == 0):
        return None
    if (len(operands) == 1):
        return operands[0]
    # (((x + y) + 2) + z)          [x, y, 2, z]
    return BinaryOpNode(packOperands(operands[:-1], operator), operator, operands[-1])

def addKeyFunc(operand):
    return (
        -getDegree(operand),
        -max([getDegree(op) for op in getOperands(operand, "*")]),
    )

def multKeyFunc(operands):
    # [False True]
    def getName(x):
        if isinstance(operands, VariableNode) or isinstance(operands, FunctionNode):
            return x.name
        return ''
    return (
        not isinstance(operands, VariableNode),
        not isinstance(operands, FunctionNode),
        not isinstance(operands, BinaryOpNode),
        getName(operands),
    )

def  getDegree(op):
    if (isinstance(op, VariableNode)):
        return 1
    if (isinstance(op, BinaryOpNode)):
        if (op.operator == "*"):
            return getDegree(op.left) + getDegree(op.right)
        if (op.operator == "/"):    
            return getDegree(op.left) - getDegree(op.right)
        if (op.operator == "^") and isinstance(op.right, NumberNode):
            # (x+1)^1/2
            return getDegree(op.left) + op.right.value
        if op.operator in ["+", "-"]:
            return max(getDegree(op.left), getDegree(op.right))
    if (isinstance(op, UnaryOpNode)):
        return getDegree(op.operand)
    return 0





