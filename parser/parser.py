from ply import yacc
from .lexer import tokens
from model import NumberNode, VariableNode, BinaryOpNode, FunctionNode, UnaryOpNode


def p_expr(p):
    '''Expr        : CompareExpr'''

    # print('Expr')
    if (len(p) == 2):
        p[0] = p[1]
        return


def p_compare_expr(p):
    '''CompareExpr : AddExpr COMPARE AddExpr
                   | AddExpr'''

    # print('CompareExpr')
    if (len(p) == 4):
        p[0] = BinaryOpNode(p[1], p[2], p[3])
        return

    if (len(p) == 2):
        p[0] = p[1]
        return


def p_add_expr(p):
    '''AddExpr     : AddExpr PLUS MulExpr
                   | AddExpr MINUS MulExpr
                   | MulExpr'''

    # print('AddExpr')
    if (len(p) == 4):
        if(p[1] == None or p[3] == None):
            p[0] = p[1] if p[3] == None else p[3]
            return
        p[0] = BinaryOpNode(p[1], p[2], p[3])
        return

    if (len(p) == 2):
        p[0] = p[1]
        return


def p_mult_expr(p):
    '''MulExpr     : MulExpr MULT PowExpr
                   | MulExpr DIV PowExpr
                   | MulExpr PowExpr2
                   | PowExpr'''

    # # print('MulExpr')
    if (len(p) == 4):
        if(p[1] == None or p[3] == None):
            p[0] = p[1] if p[3] == None else p[3]
            return
        p[0] = BinaryOpNode(p[1], p[2], p[3])
        return

    if (len(p) == 3):
        if(p[1] == None or p[2] == None):
            p[0] = p[1] if p[2] == None else p[2]
            return
        p[0] = BinaryOpNode(p[1], '*', p[2])
        return

    if (len(p) == 2):
        p[0] = p[1]
        return


def p_pow_expr(p):  
    '''PowExpr     : UnaryExpr POW PowExpr
                   | UnaryExpr'''

    # print('PowExpr')
    if (len(p) == 4):
        if(p[1] == None or p[3] == None):
            p[0] = p[1] if p[3] == None else p[3]
            return
        p[0] = BinaryOpNode(p[1], p[2], p[3])
        return

    if (len(p) == 2):
        p[0] = p[1]
        return


def p_pow_expr2(p):
    '''PowExpr2    : Primary POW PowExpr
                   | Primary'''

    # print('PowExpr2')
    if (len(p) == 4):
        if(p[1] == None or p[3] == None):
            p[0] = p[1] if p[3] == None else p[3]
            return
        p[0] = BinaryOpNode(p[1], p[2], p[3])
        return

    if (len(p) == 2):
        p[0] = p[1]
        return


def p_unary_expr(p):
    '''UnaryExpr   : PLUS UnaryExpr
                   | MINUS UnaryExpr
                   | Primary'''

    # print('UnaryExpr')
    if (len(p) == 3):
        if(p[2] == None):
            p[0] = p[2]
            return
        p[0] = UnaryOpNode(p[1], p[2])
        return

    if (len(p) == 2):
        p[0] = p[1]
        return


def p_primary(p):
    '''Primary     : Number
                   | Variable
                   | Function
                   | Group'''

    # print('Primary')
    if (len(p) == 2):
        p[0] = p[1]
        return
    
def p_number(p):
    '''Number      : NUMBER'''

    # print('Number')
    if (len(p) == 2):
        p[0] = NumberNode(p[1])
        return


def p_variable(p):
    '''Variable    : VAR'''

    # print('Variable')
    if (len(p) == 2):
        p[0] = VariableNode(p[1])
        return


def p_function(p):
    '''Function    : FUNCTION LPAREN AddExpr RPAREN
                   | FUNCTION Variable
                   | FUNCTION Number'''

    # print('Function')
    if (len(p) == 5):
        if(p[3] == None):
            p[0] = p[3]
            return
        p[0] = FunctionNode(p[1], p[3])
        return

    if (len(p) == 3):
        if(p[2] == None):
            p[0] = p[2]
            return
        p[0] = FunctionNode(p[1], p[2])
        return


def p_group(p):
    '''Group       : LPAREN AddExpr RPAREN '''

    # print('Group')
    if (len(p) == 4):
        p[0] = p[2]
        return


def p_error(p):
    if not p:
        # print("Unexpected end of file")
        return
    # print("Syntax error at '%s'" % p.value)


parser = yacc.yacc()
