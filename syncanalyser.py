# ------------------------------------------------------------
# calcparser.py
#
# parser for a simple expression evaluator for
# numbers and +,-,*,/
# ------------------------------------------------------------
import ply.yacc as yacc
from lexanalyser import tokens

# Precedence rules for the arithmetic operators
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('nonassoc', 'UMINUS'),
)

# Dictionary of names (for storing variables)
names = {}

# Helper function to create nodes
def create_node(type, *children):
    return {'type': type, 'children': list(children)}

def p_statement_expr(p):
    'statement : expression'
    p[0] = create_node('statement', p[1])

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    p[0] = create_node(p[2], p[1], p[3])

def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = create_node('UMINUS', p[2])

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = create_node('group', p[2])

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = create_node('NUMBER', p[1])

def p_expression_variable(p):
    'expression : VARIABLE'
    p[0] = create_node('VARIABLE', p[1])

def p_expression_function(p):
    'expression : FUNCTION LPAREN expression RPAREN'
    p[0] = create_node('FUNCTION', p[1], p[3])

def p_error(p):
    print("Syntax error at '%s'" % p.value)

parser = yacc.yacc()

# Helper function to print the parse tree
def print_tree(node, indent=0):
    if isinstance(node, dict):
        print('  ' * indent + f"{node['type']}")
        for child in node['children']:
            print_tree(child, indent + 1)
    else:
        print('  ' * indent + str(node))

# Test it out
data = '''sin(x+2) + log(15*y)'''

# Give the parser some input
result = parser.parse(data)

# Print the parse tree
print_tree(result)
