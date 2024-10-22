# ------------------------------------------------------------
# calclex.py
#
# tokenizer for a simple expression evaluator for
# numbers and +,-,*,/
# ------------------------------------------------------------
from ply.lex import lex, TOKEN


function = ['sin', 'cos', 'tg', 'ctg', 'ln',
            'log', 'asin', 'acos', 'atg', 'actg']
# List of token names.   This is always required
tokens = (
    'NUMBER',
    'VAR',
    'FUNCTION',
    'PLUS',
    'MINUS',
    'MULT',
    'DIV',
    'LPAREN',
    'RPAREN',
    'POW',
    'COMPARE'
)

# Regular expression rules for simple tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULT = r'\*'
t_DIV = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_POW = r'\^'
t_COMPARE = r'\=|[\>\<]\=?'

# A regular expression rule with some action code
@TOKEN(r'\d+(\.\d*)?|\.\d+')
def t_NUMBER(t):
    t.value = float(t.value)
    return t


@TOKEN('|'.join(function))
def t_FUNCTION(t):
    return t


@TOKEN(r'[a-zA-Z](_[0-9]+)?')
def t_VAR(t):
    return t

# Define a rule so we can track line numbers


@TOKEN(r'\n+')
def t_newline(t):
    t.lexer.lineno += len(t.value)


# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'

# Error handling rul


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
lexer = lex()


if __name__ == "__main__":

# Test it out
    data = '''
    sin(1) +
    '''
    # Give the lexer some input
    lexer.input(data)

    while True:
        tok = lexer.token()
        if not tok:
            break      # No more input
        print(tok)
