# courseWorkCompilers



# Лексическая структура языка 
NUMBER  -> '\[0-9]+(\.\[0-9]*)?|\.\[0-9]+'
COMPARE -> =
PLUS    -> +
MINUS   -> -
MULT    -> *
DIVIDE  -> /
POW     -> ^
LPAREN  -> (
RPAREN  -> )
FUNCTION-> 'sin' | 'cos' | 'tg' | 'ctg' | 'ln' | 'log'| 'asin'| 'acos'| 'atg'| 'actg'
VAR     -> '(pi)|[a-zA-Z](_[0-9]+)?'


# Грамматика языка 

<Expr>       |= <CompareExpr>

<CompareExpr>|= <AddExpr> COMPARE <AddExpr>
             |  <AddExpr>

<AddExpr>    |= <MultExpr> PLUS <AddExpr>
             |  <MultExpr> MINUS <AddExpr>
             |  <MultExpr>

<MultExpr>    |= <MultExpr> MULT <PowExpr>
             |  <MultExpr> DIVIDE <PowExpr>
             |  <MultExpr> <Primary>
             |  <PowExpr>

<PowExpr>    |= <UnaryExpr> POW <PowExpr>
             |  <UnaryExpr>

<UnaryExpr>  |= PLUS <UnaryExpr>
             |  MINUS <UnaryExpr>
             |  <Primary>

<Primary>    |= <Number>
             |  <Variable>
             |  <Function>
             |  <Group>

<Number>     |= NUMBER (терм символы из лексического анализа)

<Variable>   |= VAR

<Function>   |= FUNCTION LPAREN <AddExpr> RPAREN
             |  FUNCTION <Variable>

<Group>      |= LPAREN <AddExpr> RPAREN




LALR(1) (LA от англ. lookahead — предпросмотр) — восходящий алгоритм синтаксического разбора.

# Grammar
2*x + sin(y)^5 - 2

<Expr>        |= <CompareExpr>

<CompareExpr> |= <AddExpr> COMPARE <AddExpr>
              |  <AddExpr>

<AddExpr>     |= <AddExpr> PLUS <MultExpr>
              |  <AddExpr> MINUS <MultExpr>
              |  <MultExpr>

<MultExpr>    |= <MultExpr> MULT <PowExpr>
              |  <MultExpr> DIVIDE <PowExpr>
              |  <MultExpr> <PowExpr2>
              |  <PowExpr>

<PowExpr>     |= <UnaryExpr> POW <PowExpr>
              |  <UnaryExpr>

<PowExpr2>    |= <Primary> POW <PowExpr>
              |  <Primary>

<UnaryExpr>   |= PLUS <UnaryExpr>
              |  MINUS <UnaryExpr>
              |  <Primary>

<Primary>     |= <Number>
              |  <Variable>
              |  <Function>
              |  <Group>

<Number>      |= NUMBER 

<Variable>    |= VAR

<Function>    |= FUNCTION LPAREN <AddExpr> RPAREN
              |  FUNCTION <Variable>
              |  FUNCTION <Number>

<Group>       |= LPAREN <AddExpr> RPAREN
