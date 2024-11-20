from parser import parse
from simplify import simplify
from converter import convert, generate_random_numbers
from utils import print_tree, prettify


# TESTS
# 2*(x-y)^2
# 2*3(x*y)^4
# 2*3(x*y)^4
# y
# /
# x
# 
if __name__=="__main__":

    data  = '''
        x / (y / z)
    '''

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

# 
# 