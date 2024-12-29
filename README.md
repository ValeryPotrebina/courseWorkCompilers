# courseWorkCompilers



# Лексическая структура языка 
NUMBER      -> '\[0-9]+(\.\[0-9]*)?|\.\[0-9]+'
COMPARE     -> =
PLUS        -> +
MINUS       -> -
MULT        -> *
DIVIDE      -> /
POW         -> ^
LPAREN      -> (
RPAREN      -> )
FUNCTION    -> 'sin' | 'cos' | 'tg' | 'ctg' | 'ln' | 'log'| 'asin'| 'acos'| 'atg'| 'actg'
VAR         -> '(pi)|[a-zA-Z](_[0-9]+)?'


LALR(1) (LA от англ. lookahead — предпросмотр) — восходящий алгоритм синтаксического разбора.

# Grammar
    
<Expr>          |= <CompareExpr>

<CompareExpr>   |= <AddExpr> COMPARE <AddExpr>
                |  <AddExpr>

<AddExpr>       |= <AddExpr> PLUS <MultExpr>
                |  <AddExpr> MINUS <MultExpr>
                |  <MultExpr>

<MultExpr>      |= <MultExpr> MULT <PowExpr>
                |  <MultExpr> DIVIDE <PowExpr>
                |  <MultExpr> <PowExpr2>
                |  <PowExpr>

<PowExpr>       |= <UnaryExpr> POW <PowExpr>
                |  <UnaryExpr>

<PowExpr2>      |= <Primary> POW <PowExpr>
                |  <Primary>

<UnaryExpr>     |= PLUS <UnaryExpr>
                |  MINUS <UnaryExpr>
                |  <Primary>

<Primary>       |= <Number>
                |  <Variable>
                |  <Function>
                |  <Group>

<Number>        |= NUMBER 

<Variable>      |= VAR

<Function>      |= FUNCTION LPAREN <AddExpr> RPAREN
                |  FUNCTION <Variable>
                |  FUNCTION <Number>

<Group>         |= LPAREN <AddExpr> RPAREN










<!--  -->

expression  ->   expression COMPARE expression
                 expression PLUS expression  |
                 expression MINUS expression |
                 expression MULT expression  |
                 expression DIV expression   |
                 expression POW expression   | 

expression  ->   unar expression |
                 VAR | 
                 NUMBER | 
                 LPAREN expression RPAREN | 
                 
                 
                
expression  ->   unar expression            |
                 VAR                        | 
                 NUMBER                     | 
                 LPAREN expression RPAREN   |     

expression  ->   FUNCTION LPAREN expression RPAREN |
                 FUNCTION VAR          
                 
unar        ->   MINUS | PLUS   