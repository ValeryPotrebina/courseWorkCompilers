from model import BinaryOpNode, FunctionNode, NumberNode, VariableNode, UnaryOpNode
import math

multDist = ["+", "-"]

# дистрибутивность по умножению
# calc
# дистрибутивность по степени


def simplify(node):
    node = distributivity(node)
    # print("distributivity: ", node)
    node = normalize(node)
    # print("normalize: ", node)
    return node


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


def distributivity(node):
    if isinstance(node, BinaryOpNode):
        if (node.operator == "*"):
            return distributivityMult(node)
        if (node.operator == "^"):
            return distributivityPow(node)
        if (node.operator == "/"):
            # TODO: distributivityDevision
            return distributivityDevision()
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
        # 0 * x = 0
        if (isinstance(left, NumberNode) and left.value == 0):
            return NumberNode(0)
        # x * 0 = 0
        if (isinstance(right, NumberNode) and right.value == 0):
            return NumberNode(0)
        # 1 * x = x
        if (isinstance(left, NumberNode) and left.value == 1):
            return right
        # x * 1 = x
        if (isinstance(right, NumberNode) and right.value == 1):
            return left
        # Multiplication distributivity 
        if (isinstance(right, BinaryOpNode) and right.operator in ["+", "-"]):
            # x * (y +|- z) -> x * y +|- x * z
            return distributivity(BinaryOpNode(
                BinaryOpNode(left, "*", right.left),
                right.operator,
                BinaryOpNode(left, "*", right.right))
            )
        if (isinstance(left, BinaryOpNode) and left.operator in ["+", "-"]):
            # (y +|- z) * x -> y * x +|- z * x
            return distributivity(BinaryOpNode(
                BinaryOpNode(
                    left.left,
                    "*",
                    right),
                left.operator,
                BinaryOpNode(
                    left.right, 
                    "*", 
                    right))
            )
    return BinaryOpNode(
        left,
        node.operator,
        right
        )

def distributivityPow(node: BinaryOpNode):
    left = distributivity(node.left)
    right = distributivity(node.right)
    if (node.operator == "^"):
        # (че угодно)^0 = 1
        if (isinstance(right, NumberNode) and right.value == 0):
            return NumberNode(1)
        # (че угодно)^1 = (че угодно)
        if (isinstance(right, NumberNode) and right.value == 1):
            return left
        # 1^(че угодно) = 1 || 0^(че угодно) = 0
        # 0^0 - exception
        if (isinstance(left, NumberNode) and (left.value == 1 or left.value == 0)):
            return NumberNode(left.value)
        # (x*y)^n => x^n*y^n, n=число
        # (xy)^a => x^a*y^a  a=переменная
        if (isinstance(left, BinaryOpNode) and left.operator in ["*", "/"]):
            # (left.left left.operator left.right)^right.value => left.left^right.value left.operator left.right^right.value
            return (BinaryOpNode(
                # Исправила!
                distributivity(BinaryOpNode(
                    left.left,
                    node.operator,
                    right
                )),
                left.operator,
                distributivity(BinaryOpNode(
                    left.right,
                    node.operator,
                    right
                ))
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

# Не используется
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
            # TODO -(2) -> -2
            if (isinstance(node.operand, NumberNode)):
                return NumberNode(-node.operand.value)
            # TODO -(x) -> -(x)
            if (isinstance(node.operand, VariableNode)):
                return node
            # TODO -(sin(x)) -> -(sin(x))
            if (isinstance(node.operand, FunctionNode)):
                return UnaryOpNode(
                    node.operator,
                    descentUnary(node.operand)
                )
            # TODO - (- x)
            if (isinstance(node.operand, UnaryOpNode)):
                if (node.operand.operator == "-"):
                    return node.operand.operand
                if (node.operand.operator == "+"):
                    return UnaryOpNode(node.operator, descentUnary(node.operand.operand))
            if (isinstance(node.operand, BinaryOpNode)):
                if (node.operand.operator == "+"):
                    # TODO - (x + y) => -(x) + -(y)
                    return descentUnary(
                        BinaryOpNode(
                            UnaryOpNode("-", node.operand.left),
                            "+",
                            UnaryOpNode("-", node.operand.right)
                        )
                    )
                if (node.operand.operator == "-"):
                    # TODO - (x - y) => -(x) + (y)
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


# TODO getOperands - получаем массив всех операндов математического выражения
# например [VariableNode(x), VariableNode(y), BinaryOpNode(VariableNode(x), ^, NumberNode(2.0)), BinaryOpNode(VariableNode(y), ^, NumberNode(2.0))]
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
    if (isinstance(node, BinaryOpNode)):
        if (node.operator == "*"):
            return normalizeMult(node)
        if (node.operator == "+"):
            return normalizeSum(node)
        if (node.operator == "^"):
            return normalizePow(node)
        if (node.operator == "-"):
            return normalizeMinus(node)
        if (node.operator == "/"):
            # TODO: normalizeDevision
            return normalizeDevision(node)
        return BinaryOpNode(normalize(node.left), node.operator, normalize(node.right))
    if (isinstance(node, FunctionNode)):
        return normalizeFunction(node)
    if (isinstance(node, UnaryOpNode)):
        return normalizeUrary(node)
    return node

# normalizeMult
# сoeff - перемноженные все числовые ноды в операндах
# vars - мапа, которая содержит в себе key: переменная value: степени этой переменной. Например x^2*x^4 vars = {x: [2, 4]}
# В результате будет нормализовано умножение. Сначало будет число, а потом переменные по алфавиту
def normalizeMult(node):
    if (isinstance(node, BinaryOpNode) and node.operator == "*"):
        coeff = 1
        vars = {}
        others = []
        operands =  [normalize(op) for op in  getOperands(node, "*")]
        for op in operands:
            if (isinstance(op, UnaryOpNode)) and op.operator in ["+", "-"]:
                coeff *= 1 if op.operator == "+" else -1
                op = normalize(op.operand)
            if (isinstance(op, NumberNode)):
                coeff *= op.value
                continue
            if (isinstance(op, VariableNode) or isinstance(op, FunctionNode)):
                if not op in vars:
                    vars[op] = []
                vars[op] += [NumberNode(1)]
                continue
            if (isinstance(op, BinaryOpNode) and op.operator == "^"):
                if (not op.left in vars):
                    vars[op.left] = []
                vars[op.left] += [op.right]
                continue
            # TODO: добавить деление 
            others.append(op)

        if (coeff == 0):
            return NumberNode(0)

# vars {key: node, value: [coeff1, coeff2, ...]}
        for var in vars:
            # sumDegree ->
            # для каждого ключа vars запакуем массив со степенями (сложим) и нормализуем, тем самым посчитав степени
            vars[var] = normalize(packOperands(vars[var], "+"))
            
        vars = [normalize(BinaryOpNode(var, "^", vars[var]))
                for var in sorted(list(vars.keys()), key=multKeyFunc)]  # x^ 3
        print("VARS ", vars)

        coeff = [] if coeff == 1 else [NumberNode(coeff)]
        operands = coeff + vars + others
        # print("operands (mult): ", operands)
        return packOperands(operands, "*")
    return node


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


def normalizeSum(node):
    if (isinstance(node, BinaryOpNode) and node.operator == "+"):
        # vars = {key: node, value: [coeff1, coeff2, ...]}
        vars = {}
        remainder = 0
        operands = [normalize(op) for op in getOperands(node, "+")]
        # print("operands (sum): ", operands)
        for op in operands:
            if isinstance(op, NumberNode):
                remainder += op.value
                continue
            if isinstance(op, UnaryOpNode) and isinstance(op.operand, NumberNode):
                if (op.operator == "-"):
                    remainder -= op.operand
                if (op.operator == "+"):
                    remainder += op.operand
            if isinstance(op, VariableNode):
                if (not op in vars):
                    vars[op] = 0
                vars[op] += 1
                continue
            if (isinstance(op, BinaryOpNode) and op.operator == "*"):
                termOperands = getOperands(op, "*")
                print("termOperands: ", termOperands)
                coeff = termOperands[0] if isinstance(termOperands[0], NumberNode) else NumberNode(1)
                # termOperand = [2, x, y]
                # ((2 * x) * y) -> 2 * (x * y)
                monomial = termOperands[1:] if isinstance(termOperands[0], NumberNode) else termOperands
                monomial = packOperands(monomial, "*")
                print("monomial: ", monomial)
                if (not monomial in vars):
                    vars[monomial] = 0
                vars[monomial] += coeff.value
                continue

            monomial = op
            print("monomial??: ", monomial)
            if (not monomial in vars):
                vars[monomial] = 0
                # TODO: ПРОВЕРИТЬ
            vars[monomial] += 1
# key - Node, value = coeff
# return summ coeff * key

        vars = [
            normalize(BinaryOpNode(
                NumberNode(vars[monomial]),
                "*",
                monomial
            ))
            for monomial in sorted(list(vars.keys()), key=AddKeyFunc)
        ]
        print("vars (sum): ", vars)

        remainder = [] if remainder == 0 else [NumberNode(remainder)]
        operands = vars + remainder
        return packOperands(operands, "+") if len(operands) > 0 else NumberNode(0)

    return node
    # 2 * x * 4 * y * x * sin(x) -> 8 * x^2 * y *

# Only for numbers
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


def AddKeyFunc(operand):
    return (
        -getDegree(operand),
        -max([getDegree(op) for op in getOperands(operand, "*")]),
    )


def normalizeUrary(node):
    if (isinstance(node, UnaryOpNode)):
        op = normalize(node.operand)
        if (node.operator == "+"):
            return op
        if (node.operator == "-"):
            return normalize(
                BinaryOpNode(
                    NumberNode(-1),
                    "*",
                    op
                )
            )
        return UnaryOpNode(node.operator, op)
    return node


def normalizeMinus(node):
    if (isinstance(node, BinaryOpNode) and node.operator == "-"):
        left = normalize(node.left)
        right = normalize(UnaryOpNode("-", node.right))
        return normalize(
            BinaryOpNode(
                left,
                "+",
                right
            )
        )
    return node

# 2

    # 1. Сначала числа, потом переменные
    # 2. Переменные в единственном экземпляре в алф порядке (*)
    # 3. При условии одинаковой степении сложить переменные и расположить по убыванию степени


# x^2^3 = [x, 2, y]
# x^(-a) = 1/x^a


# (2^(2^3)) => 2^8
# если получим просто операнды, то мы не поймем какая ассоциативность подразумевалась изначатьно. Для этого нужен
# ((2^2)^3) = 2^6 Bin(Bin(2, ^, 2), ^, 3)
# 2^2^3 => (2^(2^3))

def getLeftOperands(node, op):
    if (isinstance(node, BinaryOpNode) and node.operator == op):
        return getLeftOperands(node.left, op) + [node.right]
    return [node]

# (1 + 2) + 3

# TODO: РАЗОБРАТЬСЯ


def normalizePow(node):
    # TODO: ДОДЕЛАТЬ
    if (isinstance(node, BinaryOpNode) and node.operator == "^"):
        operands = [normalize(op) for op in getLeftOperands(node, "^")]

        base = operands[0]
        degree = normalize(packOperands(operands[1:], "*"))

        if (isinstance(base, NumberNode)):
            if (isinstance(degree, BinaryOpNode) and (degree.operator == "*")):
                # 2^3^(x*sinx) -> 8^(x*sinx)
                degreeOps = getOperands(degree, "*")

                degreeCoeff = degreeOps[0] if isinstance(
                    degreeOps[0], NumberNode) else NumberNode(1)
                degreeOps = degreeOps[1:] if isinstance(
                    degreeOps[0], NumberNode) else degreeOps

                degree = packOperands(degreeOps, "*")
                base = NumberNode(pow(base.value, degreeCoeff.value))
            if (isinstance(degree, NumberNode)):
                return NumberNode(pow(base.value, degree.value))
            # if (isinstance(degree, BinaryOpNode) and (degree.operator == "+")):
            #     # 2^(2+xy) -> 2^2 * 2^x
            #     degreeOps = getOperands(degree, "+")
            # 1^any = 1
            if (base.value == 1):
                return NumberNode(1)
            # 0^any = 0
            if (base.value == 0):
                return NumberNode(0)

        if (isinstance(degree, NumberNode)):
            if (degree.value == 0):
                return NumberNode(1)
            if (degree.value == 1):
                return base
        return BinaryOpNode(base, "^", degree)
    return node


# (2 * X * ...* Y * 6)
# (2 + ... + 6)
#


def normalizeFunction(node):
    if (isinstance(node, FunctionNode)):
        simpleArg = normalize(node.arg)
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
# Приведение

# 1. Сложить все численные ноды 5 + x + 5 = 10 + x
# 2. Сложить все Var ноды с одинаковыми степенями   x^2 + 2x^2 = 3x^2
# 3. x * z + ... + 2*x*z -> 3*x*z
# 4. x*x + x^2 => 2x^2
# 5. (x + z) + ... + 2*(x+z)

# ((-z)*x + 6 + z*y + 5)
