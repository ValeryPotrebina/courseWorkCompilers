# courseWorkCompilers


1. Нормально ли, что используем библиотеки для построение лексического и синтаксического дерева (работа с деревом)
2. Хватит ли этого для курсовой 
3. 

1. Лексический 
2. Синтаксический (дерево)
3. Выполнение мат задач 


sin(1 + 3 + 3 + 5)

1. sin(x)  -> выводим график
2. x^2 = (<=) x + x / x + x есть решение + график (+ функции упрощения)
3. sin(x) = (x-2)^2  - алгоритмическое решение (численный методы приближенных ...) 
4. diretative()
5. 

DIGIT(INT, FLOAT)

CONST (e, pi...)

FUNCTIONS (sin, cos, tan, catan, arcsin, arccos, arctan, arccatan, ln, lg..., diretative, integral, solve...)

OPERATOR (+, -, *, /, ^, !, _)

IDENT (a-zA-Z) VAR

LPAR ( "(", "[", "{" )
RPAR ( ")", "]", "}" )

TYPE_TASK (=, <, >, ;)


KEY_WORDS ()

sin x -> sin(x)
sin x^2 + 2 -> sin(x) + 2


S -> FUNCTION

FUNCTION -> IDENT | IDENT OPERATION IDENT | E


<!-- Грамматика -->

# 1 + 2 * 3


expression  ->   expression COMPARE expression
                 expression PLUS expression  |
                 expression MINUS expression |
                 expression MULT expression  |
                 expression DIV expression   |
                 expression POW expression   | 

expression  ->   unar expression            |
                 VAR                        | 
                 NUMBER                     | 
                 LPAREN expression RPAREN   |     

expression  ->   FUNCTION LPAREN expression RPAREN |
                 FUNCTION VAR          

unar        ->   MINUS | PLUS                
            



Если только числа, то сразу вычисляем 


# Уравнения от одной переменной
x = 3 -> уравнение -> график
x^2 + 3x + 5 = 4 + x + 2x^2 -> уравнения + гравик
x^6 + x^4 + x^3 + x^2 = 3x

+ сравнения

---

y^2 = x + 3 

--












В правиле p_expression_uminus, строка %prec UMINUS используется для указания приоритета оператора унарного минуса. Это необходимо для правильного разрешения конфликтов при разборе выражений, содержащих унарные операторы.

Пояснение:
Приоритет операторов:
В математических выражениях унарные операторы, такие как унарный минус, имеют более высокий приоритет по сравнению с бинарными операторами, такими как сложение и вычитание. Например, в выражении -3 + 4, унарный минус применяется к 3 перед тем, как выполняется сложение.

Конфликты при разборе:
Без указания приоритета, парсер может неправильно интерпретировать выражения, содержащие унарные операторы. Например, без указания приоритета, выражение -3 + 4 может быть интерпретировано как -(3 + 4), что неправильно.

Использование %prec UMINUS:
Директива %prec UMINUS указывает парсеру, что унарный минус имеет приоритет, определенный как UMINUS в правилах приоритета операторов. Это помогает парсеру правильно разрешать конфликты и интерпретировать выражения.