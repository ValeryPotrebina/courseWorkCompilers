class Node():
    def __hash__(self):
        raise NotImplementedError("Subclasses should implement this!")

    def __eq__(self, other):
        raise NotImplementedError("Subclasses should implement this!")



class NumberNode(Node):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"NumberNode({self.value})"
    
    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        if isinstance(other, NumberNode):
            return self.value == other.value
        return False


class VariableNode(Node):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"VariableNode({self.name})"
    
    def __hash__(self):
        return hash(self.name)
    
    def __eq__(self, other):
        if isinstance(other, VariableNode):
            return self.name == other.name
        return False


class FunctionNode(Node):
    def __init__(self, name, arg):
        self.name = name
        self.arg = arg

    def __repr__(self):
        return f"FunctionNode({self.name}, {self.arg})"
    
    def __hash__(self):
        return hash((self.name, self.arg))

    def __eq__(self, other):
        if isinstance(other, FunctionNode):
            return self.name and self.arg
        return False
    
class BinaryOpNode(Node):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"BinaryOpNode({self.left}, {self.operator}, {self.right})"
    
    def __hash__(self):
        return hash((self.left, self.operator, self.right))

    def __eq__(self, other):
        if isinstance(other, BinaryOpNode):
            return (self.left == other.left and
                    self.operator == other.operator and
                    self.right == other.right)
        return False

class UnaryOpNode(Node):
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

    def __repr__(self):
        return f"UnaryOpNode({self.operator}, {self.operand})"

    def __hash__(self):
        return hash((self.operator, self.operand))

    def __eq__(self, other):
        if isinstance(other, UnaryOpNode):
            return self.operator == other.operator and self.operand == other.operand
        return False