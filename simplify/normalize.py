from model import BinaryOpNode, FunctionNode, NumberNode, VariableNode, UnaryOpNode
from .utils import getOperands, packOperands, getLeftOperands, addKeyFunc, multKeyFunc
import math

def normalize(node):
    if (isinstance(node, BinaryOpNode)):
        if (node.operator == "+"):
            # print("aa")
            return normalizeSum(node)
        if (node.operator == "-"):
            return normalizeMinus(node)
        if (node.operator == "*"):
            return normalizeMult(node)
        if (node.operator == "/"):
            # print("cccccc")
            return normalizeDivision(node)
        if (node.operator == "^"):
            return normalizePow(node)
        return BinaryOpNode(normalize(node.left), node.operator, normalize(node.right))
    if (isinstance(node, UnaryOpNode)):
        return normalizeUnary(node)
    if (isinstance(node, FunctionNode)):
        return normalizeFunction(node)
    return node


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
                # print("termOperands: ", termOperands)
                coeff = termOperands[0] if isinstance(termOperands[0], NumberNode) else NumberNode(1)
                # termOperand = [2, x, y]
                # ((2 * x) * y) -> 2 * (x * y)
                monomial = termOperands[1:] if isinstance(termOperands[0], NumberNode) else termOperands
                monomial = packOperands(monomial, "*")
                # print("monomial: ", monomial)
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
            for monomial in sorted(list(vars.keys()), key=addKeyFunc)
        ]
        # print("vars (sum): ", vars)

        remainder = [] if remainder == 0 else [NumberNode(remainder)]
        operands = vars + remainder
        return packOperands(operands, "+") if len(operands) > 0 else NumberNode(0)

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
        # print("VARS ", vars)

        coeff = [] if coeff == 1 else [NumberNode(coeff)]
        operands = coeff + vars + others
        # print("operands (mult): ", operands)
        return packOperands(operands, "*")
    return node

def normalizeDivision(node):
    # print("BBBBBBB")
    if isinstance(node, BinaryOpNode) and node.operator == "/":
        left = normalize(node.left)
        # print("left: ", left)
        right = normalize(node.right)
        # print("right: ", right)
        # (x + 1) / (x + 1) = 1
        if (left == right):
            return NumberNode(1)
        # 4 / 2 = 2
        if (isinstance(left, NumberNode) and isinstance(right, NumberNode)):
            return NumberNode(left.value / right.value)
        if (isinstance(left, BinaryOpNode) and left.operator in ["+", "-", "*"]):
            # print("AAAAAAAA")
            return BinaryOpNode(
                normalize(BinaryOpNode(left.left, "/", right)),
                left.operator,
                normalize(BinaryOpNode(left.right, "/", right))
            )
    return node



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

def normalizeUnary(node):
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
