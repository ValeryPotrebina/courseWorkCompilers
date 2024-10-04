class Node:
    # def parts_str(self):
    #     st = []
    #     for part in self.parts:
    #         st.append(str(part))
    #     return "\n".join(st)

    # def __repr__(self):
    #     return self.type + ":\n\t" + self.parts_str().replace("\n", "\n\t")

    # def add_parts(self, parts):
    #     self.parts += parts
    #     return self

    # def __init__(self, type, parts):
    #     self.type = type
    #     self.parts = parts
    pass


class NumberNode(Node):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"NumberNode({self.value})"


class VariableNode(Node):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"VariableNode({self.name})"


class FunctionNode(Node):
    def __init__(self, name, arg):
        self.name = name
        self.arg = arg

    def __repr__(self):
        return f"FunctionNode({self.name}, {self.arg})"


class BinaryOpNode(Node):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"BinaryOpNode({self.left}, {self.operator}, {self.right})"


class UnaryOpNode(Node):
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

    def __repr__(self):
        return f"UnaryOpNode({self.operator}, {self.operand})"
