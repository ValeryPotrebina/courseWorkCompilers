from model import BinaryOpNode, FunctionNode, NumberNode, VariableNode, UnaryOpNode, ConstantNode

def print_tree(node, level=0):
    indent = "  " * level
    if isinstance(node, NumberNode):
        print(f"{indent}NumberNode({node.value})")
    elif isinstance(node, ConstantNode):
        print(f"{indent}ConstantNode({node.name})")
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
    if isinstance(node, VariableNode) or isinstance(node, ConstantNode):
        return f"{node.name}"
    if isinstance(node, FunctionNode):
        return f"{node.name}({prettify(node.arg)})"
    if isinstance(node, BinaryOpNode):
        left = prettify(node.left)
        right = prettify(node.right)

        # Определяем приоритеты операторов
        operator_precedence = {
            '=': 0,  # Оператор присваивания имеет самый низкий приоритет
            '+': 1,
            '-': 1,
            '*': 2,
            '/': 2,
            '^': 3
        }

        # Проверяем приоритеты и удаляем лишние скобки
        if isinstance(node.left, BinaryOpNode) and node.operator in operator_precedence and node.left.operator in operator_precedence:
            if operator_precedence[node.operator] > operator_precedence[node.left.operator]:
                left = f"({left})"
        if isinstance(node.right, BinaryOpNode) and node.operator in operator_precedence and node.right.operator in operator_precedence:
            if operator_precedence[node.operator] > operator_precedence[node.right.operator]:
                right = f"({right})"

        return f"{left} {node.operator} {right}"
    if isinstance(node, UnaryOpNode):
        return f"{node.operator}{prettify(node.operand)}"