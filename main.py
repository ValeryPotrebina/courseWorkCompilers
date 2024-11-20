from parser import parse
from simplify import simplify
from converter import convert, generate_random_numbers
from utils import print_tree, prettify


# TESTS
# 2*(x-y)^2
# 2*3(x*y)^4
# 2*3(x*y)^4
if __name__=="__main__":
    data  = '''
        (4 + x) / 4
    '''

    # 2(x-y)(x-y)
    # 2(xx-xy-yx+yy)=2xx-2xy-2yx+2yy
    # -(zx - zy) -> -zx + zy
    # (2 * (y + z))*x -> (2y + 2z)x = 2yx + 2xz
    # (2 * (y + z))*(x + 5) -> (2yx + 2xz)(x + 5) -> ?
    # ((x + y) + z)(a + b) ?
    # (a + b)*(c + d) -> (a+b)c + (a+b)d
    # - (z * (x - y)) ->  (zx - zy) 

    result = parse(data)
    result = simplify(result)
    print_tree(result)
    print(prettify(result))

    vars, func = convert(result)
    vars_length = len(vars)
    args = generate_random_numbers(vars_length)
    result = func(args)
    print(args)
    print(result)  # Вывод: sin(1) + 2 * 2

    # operands = getOperands(result, "+")
    # print("operands (main): ", operands)



'''
1. Решить уравнение
2. Вывести график
3. Сервак подрубить 
'''