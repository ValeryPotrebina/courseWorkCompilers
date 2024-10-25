from model import BinaryOpNode, FunctionNode, NumberNode, VariableNode, UnaryOpNode
import math

commutativeOps = ["+", "*"]
associativeOps = ["+", "*"]
multDist = ["+", "-"]

def simplify(node):
    a = simpleCalculation(node)
    print(a)
    b = distributivity(a)
    print(b)
    c = descentUnary(b)
    return c


def simpleCalculation(node):
    if (isinstance(node, VariableNode) or isinstance(node, NumberNode)):
        return node
    if (isinstance(node, BinaryOpNode)):
        simpleLeft = simpleCalculation(node.left)
        simpleRight = simpleCalculation(node.right)
        if (isinstance(simpleLeft, NumberNode) and isinstance(simpleRight, NumberNode)):
            if (node.operator == "+"):
                return NumberNode(simpleLeft.value + simpleRight.value)
            if (node.operator == "-"):
                return NumberNode(simpleLeft.value - simpleRight.value)
            if (node.operator == "*"):
                return NumberNode(simpleLeft.value * simpleRight.value)
            if (node.operator == "/"):
                return NumberNode(simpleLeft.value / simpleRight.value)
            if (node.operator == "^"):
                return NumberNode(math.pow(simpleLeft.value, simpleRight.value))
        return BinaryOpNode(simpleLeft, node.operator, simpleRight)
    if (isinstance(node, UnaryOpNode)):
        simpleOperand = simpleCalculation(node.operand)
        if (isinstance(simpleOperand, NumberNode)):
            if (node.operator == "+"):
                return NumberNode(simpleOperand.value)
            if (node.operator == "-"):
                return NumberNode(-simpleOperand.value)
        return UnaryOpNode(node.operator, simpleOperand)
    if (isinstance(node, FunctionNode)):
        simpleArg = simpleCalculation(node.arg)
        if (isinstance(simpleArg, NumberNode)):
            if (node.name) == "sin":
                return NumberNode(math.sin(simpleArg.value))
            if (node.name) == "cos":
                return NumberNode(math.cos(simpleArg.value))
            if (node.name) == "tg":
                return NumberNode(math.tan(simpleArg.value))
            if (node.name) == "ctg":
                return NumberNode(1 / math.tan(simpleArg.value))
            if (node.name) == "asin":
                return NumberNode(math.asin(simpleArg.value))
            if (node.name) == "acos":
                return NumberNode(math.acos(simpleArg.value))
            if (node.name) == "atg":
                return NumberNode(math.atan(simpleArg.value))
            if (node.name) == "actg":
                return NumberNode((math.pi / 2) - math.atan(simpleArg.value))
            if (node.name) == "ln":
                return NumberNode(math.log(simpleArg.value))
            if (node.name) == "lg":
                return NumberNode(math.log10(simpleArg.value))
        return FunctionNode(node.name, simpleArg)
    return node
    # sin (2 + 3)


def commutativity(node):
    if (isinstance(node, BinaryOpNode) and (node.operator in commutativeOps)):
        return BinaryOpNode(node.right, node.operator, node.left)
    return node


def associativity(node):
    if (isinstance(node, BinaryOpNode) and node.operator in associativeOps):
        if (isinstance(node.left, BinaryOpNode) and node.left.operator == node.operator):
            # Левая ассоциативность (a + b) + c -> a + (b + c)
            # (+ (+ a b) c) -> (+ a (+ b c))
            return BinaryOpNode(node.left.left, node.operator, BinaryOpNode(node.left.right, node.operator, node.right))
        if (isinstance(node.right, BinaryOpNode) and node.right.operator == node.operator):
            return BinaryOpNode(BinaryOpNode(node.left, node.operator, node.right.left), node.operator, node.right.right)


# 5 - 2 - 3
# - x
# (* x (+ 2 4)) -> (* x 6)
# (2^3)^4 (8^4) = 2^(3^4) (2^81)

def distributivity(node):
    print("test1")
    if isinstance(node, BinaryOpNode):
        left = distributivity(node.left)
        right = distributivity(node.right)
        if node.operator == "*":
            if (isinstance(right, BinaryOpNode) and right.operator in multDist):
                print("check")
                # x * (y + z) -> x * y + x * z
                return BinaryOpNode(
                    distributivity(BinaryOpNode(left, "*", right.left)),
                    right.operator,
                    distributivity(BinaryOpNode(left, "*", right.right))
                )
            if (isinstance(left, BinaryOpNode) and left.operator in multDist):
                print("check")
                # (y + z) * x -> x * y + x * z
                return BinaryOpNode(
                    distributivity(BinaryOpNode(left.left, "*", right)),    
                    left.operator,
                    distributivity(BinaryOpNode(left.right, "*", right))
                )
        return BinaryOpNode(left, node.operator, right)
    if (isinstance(node, UnaryOpNode)):
        
        return UnaryOpNode(node.operator, distributivity(node.operand))
    if (isinstance(node, FunctionNode)):
        return FunctionNode(node.name, distributivity(node.arg))
    return node



def descentUnary(node):
    if (isinstance(node, NumberNode) or isinstance(node, VariableNode)):
        return node
    if (isinstance(node, FunctionNode)):
        return FunctionNode(node.name, descentUnary(node.arg))
    if (isinstance(node, BinaryOpNode)):
        return BinaryOpNode(descentUnary(node.left), node.operator, descentUnary(node.right))
    if (isinstance(node, UnaryOpNode)):
        if (node.operator == "-"):
            # -(2) -> -2
            if (isinstance(node.operand, NumberNode)):
                return NumberNode(-node.operand.value)
            # -(x) -> -(x)
            if (isinstance(node.operand, VariableNode)):
                return node
            # -(sin(x)) -> -(sin(x))
            if (isinstance(node.operand, FunctionNode)):
                return UnaryOpNode(node.operator, descentUnary(node.operand))
            # - (- x)
            if (isinstance(node.operand, UnaryOpNode)):
                if (node.operand.operator == "-"):
                    return node.operand.operand
                if (node.operand.operator == "+"):  
                    return UnaryOpNode(node.operator, descentUnary(node.operand.operand))
            if (isinstance(node.operand, BinaryOpNode)):
                if (node.operand.operator == "+"):
                    # - (x + y) => -(x) + -(y)
                    return descentUnary(BinaryOpNode(
                        UnaryOpNode("-", node.operand.left), 
                        "+", 
                        UnaryOpNode("-", node.operand.right)))
                if (node.operand.operator == "-"):
                    # - (x - y) => -(x) + (y)
                    return descentUnary(BinaryOpNode(
                        UnaryOpNode("-", node.operand.left), 
                        "+", 
                        (node.operand.right)))
                # - (x * y) = -x * y
                if (node.operand.operator == "*"):
                    return descentUnary(
                        BinaryOpNode(
                            UnaryOpNode("-", node.operand.left), 
                            "*", 
                            node.operand.right
                        )
                    )
                if (node.operand.operator == "/"):
                    return descentUnary(
                        BinaryOpNode(
                            UnaryOpNode("-", node.operand.left), 
                            "/", 
                            node.operand.right
                        ))
                    
                # - (BinOp(* Var(x), BinOp(* z, y)))      -> -(x * -z * y) = -x*y*z
                # - (BinOp(+ x, y))                       -> -(x + y) = -x + -y


    # - (z * (x + y))
    # дистрибутивност по умножению
    # (x + 4) * (x + y + z) or (x + y + z) x  ->>> (+ (+ x y) z) = (+ x y z)
    # (* (+ x + y)(+ x z))




