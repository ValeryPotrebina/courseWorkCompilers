from model import BinaryOpNode, FunctionNode, NumberNode, VariableNode, UnaryOpNode, ConstantNode
import re

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


preceedences = {
    '=': 0,
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2,
    '^': 3
}

left_assoc = ['+', '*', '/', '-', '=']
right_assoc = ['+', '*', '^', '=']


def toLatex(node):
    if isinstance(node, NumberNode):
        return f"{re.sub(r'\.?0*$', '', str(node.value))}"
    if isinstance(node, VariableNode) or isinstance(node, ConstantNode):
        return f"{node.name}"
    if isinstance(node, FunctionNode):
        arg = toLatex(node.arg)
        return f"{node.name}\\left({arg}\\right)"
    if isinstance(node, BinaryOpNode):
        left = toLatex(node.left)
        right = toLatex(node.right)

        if node.operator == '/':
            return f"\\frac{{{left}}}{{{right}}}"
        if node.operator == '^':
            return f"{{{left}}} ^ {{{right}}}"
        if isinstance(node.left, BinaryOpNode) and node.operator in preceedences and node.left.operator in preceedences:
            if ((preceedences[node.operator] > preceedences[node.left.operator]) or (preceedences[node.operator] == preceedences[node.left.operator] and not node.operator in left_assoc)):
                left = f"\\left({left}\\right)"
        if isinstance(node.right, BinaryOpNode) and node.operator in preceedences and node.right.operator in preceedences:
            if (preceedences[node.operator] > preceedences[node.right.operator]) or (preceedences[node.operator] == preceedences[node.right.operator] and not node.operator in right_assoc):
                right = f"\\left({right}\\right)"

        return f"{left} {node.operator} {right}"
    if isinstance(node, UnaryOpNode):
        operand = toLatex(node.operand)
        if node.operator == '-':
            return f"-{operand}"
        return operand
