import traceback
from analyzer import analyze
from parser import parse
from simplify import simplify
from converter import convert
from utils import print_tree, prettify


    
if __name__=="__main__":
    expression = "sin(x)^2 + 2*x*x + 5 + 5*x*x + 5 + sin(x)^2"
    result = parse(expression)
    f_letter, result = simplify(result)
    print(f_letter, prettify(result))

    


# TESTS
# 2*(x-y)^2
# 2*3(x*y)^4
# 2*3(x*y)^4
# y
# /
# x
# 

# 
# sin(x)  ----> Добавить pi в ответ TODO Доработать (-)
# x^3-6*x^2+11*x-6 (+)
# e^x-1      ----->Добавить e, pi (-)
# log(x)(-)
# x^4 - 64 (+) но нет комплексных чисел
# x^2 + y^2 + z^2 - 1
