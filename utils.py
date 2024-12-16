from model import BinaryOpNode, FunctionNode, NumberNode, VariableNode, UnaryOpNode

def print_tree(node, level=0):
    indent = "  " * level
    if isinstance(node, NumberNode):
        print(f"{indent}NumberNode({node.value})")
    elif isinstance(node, VariableNode):
        print(f"{indent}VariableNode({node.name})")
    elif isinstance(node, FunctionNode):
        print(f"{indent}FunctionNode({node.name})")
        print_tree(node.arg, level + 1)
    elif isinstance(node, BinaryOpNode):
        print(f"{indent}BinaryOpNode({node.operator})")
        print_tree(node.left, level + 1)
        print_tree(node.right, level + 1)
    elif isinstance(node, UnaryOpNode):
        print(f"{indent}UnaryOpNode({node.operator})")
        print_tree(node.operand, level + 1)


def prettify(node):
    if isinstance(node, NumberNode):
        return f"{node.value}"
    if isinstance(node, VariableNode):
        return f"{node.name}"
    if isinstance(node, FunctionNode):
        return f"{node.name}({prettify(node.arg)})"
    if isinstance(node, BinaryOpNode):
        left = prettify(node.left)
        if isinstance(node.left, BinaryOpNode) and node.operator in ["+", "-", "*", "/", "^"] and node.left.operator == node.operator:
            left = left[1:-1]
        right = prettify(node.right)
        if isinstance(node.right, BinaryOpNode) and node.operator in ["+", "-"] and node.right.operator == node.operator:
            right = right[1:-1]
        return f"({left} {node.operator} {right})"
    if isinstance(node, UnaryOpNode):
        return f"({node.operator}{prettify(node.operand)})"

