from model import BinaryOpNode, FunctionNode, NumberNode, VariableNode, UnaryOpNode
import math

commutativeOps = ["+", "*"]
associativeOps = ["+", "*"]
multDist = ["+", "-"]

# дистрибутивность по умножению
# calc
# дистрибутивность по степени


def simplify(node):
    a = distributivity(simpleCalculation(node))
    print("simpleCalculation", a)
    b = simpleCalculation(a)
    print("distributivity", b)
    c = descentUnary(b)
    print("descentUnary", c)
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
    if isinstance(node, BinaryOpNode):
        if (node.operator == "*"):
            return distributivityMult(node)
        if (node.operator == "^"):
            return distributivityPow(node)
        return BinaryOpNode(
            distributivity(node.left),
            node.operator,
            distributivity(node.right))
    if (isinstance(node, UnaryOpNode)):
        return UnaryOpNode(
            node.operator,
            distributivity(node.operand))
    if (isinstance(node, FunctionNode)):
        return FunctionNode(node.name, distributivity(node.arg))
    return node


def distributivityMult(node: BinaryOpNode):
    left = distributivity(node.left)
    right = distributivity(node.right)
    if node.operator == "*":
        if (isinstance(left, NumberNode) and left.value == 0):
            return NumberNode(0)
        if (isinstance(right, NumberNode) and right.value == 0):
            return NumberNode(0)
        if (isinstance(left, NumberNode) and left.value == 1):
            return right
        if (isinstance(right, NumberNode) and right.value == 1):
            return left
        if (isinstance(right, BinaryOpNode) and right.operator in multDist):
            # x * (y + z) -> x * y + x * z
            return distributivity(BinaryOpNode(
                BinaryOpNode(left, "*", right.left),
                right.operator,
                BinaryOpNode(left, "*", right.right))
            )
        if (isinstance(left, BinaryOpNode) and left.operator in multDist):
            # (y + z) * x -> x * y + x * z
            return distributivity(BinaryOpNode(
                BinaryOpNode(left.left, "*", right),
                left.operator,
                BinaryOpNode(left.right, "*", right))
            )
    return BinaryOpNode(
        left,
        node.operator,
        right)


def distributivityPow(node: BinaryOpNode):
    left = distributivity(node.left)
    right = distributivity(node.right)
    if (node.operator == "^"):
        # x^0 = 1
        if (isinstance(right, NumberNode) and right.value == 0):
            return NumberNode(1)
        # 1^(че угодно) = 1 || 0^(че угодно) = 0
        if (isinstance(left, NumberNode) and (left.value == 1 or left.value == 0)):
            return NumberNode(left.value)
        # (x*y)^n => x^n*y^n, n=число
        # (xy)^a => x^a*y^a  a=переменная
        if (isinstance(left, BinaryOpNode) and left.operator in ["*", "/"]):
            # (left.left left.operator left.right)^right.value => left.left^right.value left.operator left.right^right.value
            return distributivity(BinaryOpNode(
                BinaryOpNode(
                    left.left,
                    node.operator,
                    right
                ),
                left.operator,
                BinaryOpNode(
                    left.right,
                    node.operator,
                    right
                )
            ))

        # (x+y)^n => (x+y)*(x+y)^(n-1), n=число
        # (x+y)^a => оставляем также a=переменная
        if (isinstance(left, BinaryOpNode) and left.operator in ["+", "-"]) and isinstance(right, NumberNode):
            # (x+y)^n => (x+y)*(x+y)^(n-1)
            return distributivity(
                BinaryOpNode(
                    left,
                    "*",
                    BinaryOpNode(
                        left, 
                        node.operator, 
                        NumberNode(right.value - 1)
                    )
                )
            )
    return BinaryOpNode(left, node.operator, right)


# -1(x + y) => -x -y

        # (x+y)^n => (x+y)*(x+y)^(n-1), n=число
        # (x+y)^a => оставляем также a=переменная

        # x^(a+b)=> x^a*x^b

def descentUnary(node):
    if (isinstance(node, NumberNode) or isinstance(node, VariableNode)):
        return node
    if (isinstance(node, FunctionNode)):
        return FunctionNode(node.name, descentUnary(node.arg))
    if (isinstance(node, BinaryOpNode)):
        # a - b = a + (-b)
        if (node.operator == "-"):
            return descentUnary(
                BinaryOpNode(
                    node.left, 
                    "+",
                    UnaryOpNode("-", node.right)
                )
            )
        return BinaryOpNode(
            descentUnary(node.left), 
            node.operator, 
            descentUnary(node.right))
    if (isinstance(node, UnaryOpNode)):
        if (node.operator == "+"):
            return node.operand
        if (node.operator == "-"):
            # -(2) -> -2
            if (isinstance(node.operand, NumberNode)):
                return NumberNode(-node.operand.value)
            # -(x) -> -(x)
            if (isinstance(node.operand, VariableNode)):
                return node
            # -(sin(x)) -> -(sin(x))
            if (isinstance(node.operand, FunctionNode)):
                return UnaryOpNode(
                    node.operator, 
                    descentUnary(node.operand)
                )
            # - (- x)
            if (isinstance(node.operand, UnaryOpNode)):
                if (node.operand.operator == "-"):
                    return node.operand.operand
                if (node.operand.operator == "+"):
                    return UnaryOpNode(node.operator, descentUnary(node.operand.operand))
            if (isinstance(node.operand, BinaryOpNode)):
                if (node.operand.operator == "+"):
                    # - (x + y) => -(x) + -(y)
                    return descentUnary(
                        BinaryOpNode(
                            UnaryOpNode("-", node.operand.left),
                            "+",
                            UnaryOpNode("-", node.operand.right)
                        )
                    )
                if (node.operand.operator == "-"):
                    # TODO
                    # - (x - y) => -(x) + (y)
                    return descentUnary(
                        BinaryOpNode(
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
        return UnaryOpNode(node.operator, descentUnary(node.operand))            

                # - (BinOp(* Var(x), BinOp(* z, y)))      -> -(x * -z * y) = -x*y*z
                # - (BinOp(+ x, y))                       -> -(x + y) = -x + -y

    # - (z * (x + y))
    # дистрибутивност по умножению
    # (x + 4) * (x + y + z) or (x + y + z) x  ->>> (+ (+ x y) z) = (+ x y z)
    # (* (+ x + y)(+ x z))

# BiOp(Num(6) * BiOp(x * BiOp(x * Num(3)))) (6 * x * 4 * x * 3) -> (18 * x^2)
# (6 * x^2 * x * 3) -> (18 x^3)
# (6*x + 3 + (x^3 + x^2 + x/y + x + 3x + 5)) -> 

def getOperands(node, operator):
    if (isinstance(node, BinaryOpNode) and node.operator == operator):
        return getOperands(node.left, operator) + getOperands(node.right, operator)
    return [node]


def packOperands(operands, operator):
    if (len(operands) == 0):
        return None
    if (len(operands) == 1):
        return operands[0]
    # (((x + y) + 2) + z)          [x, y, 2, z]
    return BinaryOpNode(packOperands(operands[:-1], operator), operator, operands[-1])


def normalize(node):
    return

# Правила для степений
# x^1 = x
# x^0 = 1
# x^a * x^b = x^(a+b)
# x


def normalizeMult(node):
    # перестроить дерево 
    # 
    if (isinstance(node, BinaryOpNode) and node.operator == "*"):
        coeff = 1
        # key - variable.name value - array(node)
        vars = {}
        others = []
        operands = getOperands(node, "*")
        for op in operands:
            if (isinstance(op, NumberNode)):
                coeff *= op.value
                continue
            #  x^2*x
            # vars [x : Num(1)]  x*x^y => x^(1+y)  
            #   
            # x^(1 + y + 2)  
            # x []
            if (isinstance(op, VariableNode)):  
                if vars.get(op.name) is None:
                    vars[op.name] = []
                vars[op.name] += [NumberNode(1)]
                continue
            if (isinstance(op, UnaryOpNode)):
                if (op.operator == "-"):
                    coeff *= -1
                continue
            if (isinstance(op, BinaryOpNode) and op.operator == "^" and isinstance(op.left, VariableNode)):
                if (op.left.name is None):
                    vars[op.left.name] = []
                vars[op.left.name] += [op.right]
                continue
            others.append(op)

        for var in vars:
            # x^1*x^2
            # vars = {x [1, 2]}
            # Binar(..., +, ...)
            # deg -> BinaryOp
            vars[var] = normalizeSum(packOperands(vars[var], "+")) 

        # Собрать ноду
        # ORDER : NUMBER VARIABLE1 VARIABLE2 (ALPHABET PRDER)
        
        vars = [BinaryOpNode(VariableNode(var), "^", vars[var]) for var in sorted(list(vars.keys()))] # x^ 3

        coeff = [] if coeff == 1 else [NumberNode(coeff)]
        operands = coeff + vars + others
        # [1, x, y, cos]
        result = packOperands(operands, "*")
        return result
    return node   


def normalizeSum(node):
    return node   
    if (isinstance(node, BinaryOpNode) and node.operator == "+"):
        vars = {}
        remainder = 0
        operands = getOperands(node, "+")
        for op in operands:
            if isinstance(op, NumberNode):
                remainder += op.value
                continue
            if isinstance(op, VariableNode):
                # x + y + x^2 --> vars{x: Var(x), Bin(x)}
                # x + 2x [key x, value {1, 2}]
                # x^2 + 2x^2 [key x^2, value: {1, 2}]
                # x^3*y^4*z^5 + 4*x^3*y^4*z^5 = [key: x^3*y^4*z^5, value : [1, 4]]
                # x^y*z^y + 4*z^y*x^y -> [key "x^y*z^y"]
                if (vars[op.name] in None):
                    vars[op.name] = []
                vars[op.name] += []
                continue
            if (isinstance(op, BinaryOpNode) and op.operator == "^"):
                return
     
            
        # 2 * x * 4 * y * x * sin(x) -> 8 * x^2 * y * 



    # 1. Сначала числа, потом переменные
    # 2. Переменные в единственном экземпляре в алф порядке (*)
    # 3. При условии одинаковой степении сложить переменные и расположить по убыванию степени


def pow(node):
    return



# (2 * X * ...* Y * 6)
# (2 + ... + 6)
# 




# Приведение

# 1. Сложить все численные ноды 5 + x + 5 = 10 + x
# 2. Сложить все Var ноды с одинаковыми степенями   x^2 + 2x^2 = 3x^2
# 3. x * z + ... + 2*x*z -> 3*x*z
# 4. x*x + x^2 => 2x^2
# 5. (x + z) + ... + 2*(x+z)

# ((-z)*x + 6 + z*y + 5)
