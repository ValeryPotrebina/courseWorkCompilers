# ------------------------------------------------------------
# calcparse.py
#
# parser for a simple expression evaluator for
# numbers and +,-,*,/
# ------------------------------------------------------------
from ply import yacc
from lexer import tokens
from model import NumberNode, VariableNode, BinaryOpNode, FunctionNode, UnaryOpNode

# ЗАЧЕМ НАМ СЛОВАРЬ
names = {}

# КАК РАБОТАЮТ ПРИОРИТЕТЫ
precedence = (
    ('left', 'COMPARE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULT', 'DIV'),
    ('right', 'POW'),
    ('nonassoc', 'UMINUS'),
)


# def p_statement_expt(p):
#     'statement : expression'
#     print(p[1])


def p_calc(p):
    '''expression : expression COMPARE expression
                  | expression PLUS expression
                  | expression MINUS expression 
                  | expression MULT expression  
                  | expression DIV expression   
                  | expression POW expression'''
    # p[0] = p[1] + p[3]
    p[0] = BinaryOpNode(p[1], p[2], p[3])
    # print(p[0], p[1], p[2], p[3])


def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]


def p_expression_var(p):
    'expression : VAR'
    p[0] = VariableNode(p[1])


def p_expression_num(p):
    'expression : NUMBER'
    p[0] = NumberNode(p[1])


def p_expression_uminus(p):
    # Указываем приоритет унарного минуса
    'expression : MINUS expression %prec UMINUS'
    p[0] = UnaryOpNode('-', p[2])


def p_expression_function(p):
    '''expression : FUNCTION LPAREN expression RPAREN
                  | FUNCTION VAR '''
    if (len(p) == 5):
        p[0] = FunctionNode(p[1], p[3])
    else:
        p[0] = FunctionNode(p[1], p[2])



def p_error(p):
    print("Syntax error at '%s'" % p.value)


def print_tree(node, level=0):
    indent = "  " * level
    if isinstance(node, NumberNode):
        print(f"{indent}Number({node.value})")
    elif isinstance(node, VariableNode):
        print(f"{indent}Variable({node.name})")
    elif isinstance(node, FunctionNode):
        print(f"{indent}Function({node.name})")
        print_tree(node.arg, level + 1)
    elif isinstance(node, BinaryOpNode):
        print(f"{indent}BinaryOp({node.operator})")
        print_tree(node.left, level + 1)
        print_tree(node.right, level + 1)
    elif isinstance(node, UnaryOpNode):
        print(f"{indent}UnaryOp({node.operator})")
        print_tree(node.operand, level + 1)



def parse(data):
    return parser.parse(data)
# Build the parser
parser = yacc.yacc()

def prettify(node):
    if isinstance(node, NumberNode):
        return f"{node.value}"
    if isinstance(node, VariableNode):
        return f"{node.name}"
    if isinstance(node, FunctionNode):
        return f"{node.name}({prettify(node.arg)})"
    if isinstance(node, BinaryOpNode):
        left = prettify(node.left)
        if isinstance(node.left, BinaryOpNode) and node.left.operator == node.operator:
            left = left[1:-1]
        right = prettify(node.right)
        if isinstance(node.right, BinaryOpNode) and node.right.operator == node.operator:
            right = right[1:-1]
        return f"({left} {node.operator} {right})"
    if isinstance(node, UnaryOpNode):
        return f"({node.operator}{prettify(node.operand)})"


if __name__ == "__main__":
    data = '''x + y * 2'''
    data1 = '''(x + y) * 2'''
    data2 = '''-(x + y) * 2'''
    data3 = '''sin(x+1) + ln(y+x)'''
    data4 = '''x^(2+y)'''

    # data5 = '''sin(x+1) + ln(x)'''  Неработает

    # Give the parser some input
    result = parse(data)
    result1 = parse(data1)
    result2 = parse(data2)
    result3 = parse(data3)
    result4 = parse(data4)


    print_tree(result)
    print("------------------")
    print_tree(result1)
    print("------------------")
    print_tree(result2)
    print("------------------")
    print_tree(result3)
    print("------------------")
    print_tree(result4)


