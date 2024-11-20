from model import BinaryOpNode, FunctionNode, NumberNode, VariableNode, UnaryOpNode

def distributivity(node):
    if isinstance(node, BinaryOpNode):
        if (node.operator == "*"):
            return distributivityMult(node)
        if (node.operator == "^"):
            return distributivityPow(node)
        if (node.operator == "/"):
            return distributivityDivision(node)
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

def distributivityDivision(node):
    left = distributivity(node.left)
    right = distributivity(node.right)
    if node.operator == "/":
        # 0 / x = 0
        if (isinstance(left, NumberNode) and left.value == 0):
            return NumberNode(0)
        # x / 0 = 0
        # if (isinstance(right, NumberNode) and right.value == 0):
        #     return 
        # x / 1 = x
        if (isinstance(right, NumberNode) and right.value == 1):
            return left
        # division distributivity 
        if (isinstance(left, BinaryOpNode) and left.operator in ["+", "-"]):
            # (y +|- z) / x -> y * x +|- z * x
            return distributivity(BinaryOpNode(
                BinaryOpNode(
                    left.left,
                    "/",
                    right),
                left.operator,
                BinaryOpNode(
                    left.right, 
                    "/", 
                    right))
            )
    return BinaryOpNode(
        left,
        node.operator,
        right
        )
