from ply import yacc
from .lexer import tokens
from model import NumberNode, VariableNode, BinaryOpNode, FunctionNode, UnaryOpNode

names = {}

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
    p[0] = BinaryOpNode(p[1], p[2], p[3])


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


parser = yacc.yacc()



