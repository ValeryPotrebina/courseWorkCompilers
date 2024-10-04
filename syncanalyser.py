# ------------------------------------------------------------
# calcparse.py
#
# parser for a simple expression evaluator for
# numbers and +,-,*,/
# ------------------------------------------------------------
from ply import yacc
from lexanalyser import tokens
from model import NumberNode, VariableNode, BinaryOpNode, FunctionNode, UnaryOpNode

# ЗАЧЕМ НАМ СЛОВАРЬ
names = {}

# КАК РАБОТАЮТ ПРИОРИТЕТЫ
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULT', 'DIV'),
    ('right', 'POW'),
    ('nonassoc', 'UMINUS'),
)


# def p_statement_expt(p):
#     'statement : expression'
#     print(p[1])


def p_calc(p):
    '''expression : expression PLUS expression
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
        print(f"{indent}UnaryOp{node.operator})")
        print_tree(node.operand, level + 1)


# Build the parser
parser = yacc.yacc()

# Test it out
data = '''x + y * 2'''
data1 = '''(x + y) * 2'''
data2 = '''-(x + y) * 2'''
data3 = '''sin(x+1) + ln(y+x)'''
# data5 = '''sin(x+1) + ln(x)'''  Неработает

# Give the parser some input
result = parser.parse(data)
result1 = parser.parse(data1)
result2 = parser.parse(data2)
result3 = parser.parse(data3)

print_tree(result)
print("------------------")
print_tree(result1)
print("------------------")
print_tree(result2)
print("------------------")
print_tree(result3)
