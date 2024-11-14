from model import BinaryOpNode, FunctionNode, NumberNode, VariableNode, UnaryOpNode

def collectVariables(node):
    if isinstance(node, NumberNode):
        return []
    if isinstance(node, VariableNode):
        return [node.name]
    if isinstance(node, FunctionNode):
        return collectVariables(node.arg)
    if isinstance(node, BinaryOpNode):
        return list(set(collectVariables(node.left) + collectVariables(node.right)))
    if isinstance(node, UnaryOpNode):
        return collectVariables(node.operand)
    return []

def convert(node):
    vars = sorted(collectVariables(node))
    return convertNode(node, vars)


# def convertNode(node, vars):
#     if (isinstance(node, NumberNode)):
#         return node.value
#     if (isinstance(node, VariableNode)):    
#         return lambda args: args[vars.index(node.name)]
#         if (node.operator == "+"):

