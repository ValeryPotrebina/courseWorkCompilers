import traceback
from analyzer import analyze
from parser import parse
from simplify import simplify
from converter import convert
from utils import print_tree, prettify


    
if __name__=="__main__":
    expression1 = "sin(x)^2 + 2*x*x + 5 + 5*x*x + 5 + sin(x)^2 "
    expression2 = "sin(1)^2 + cos(1)^2"
    expression3 = "2^(2*y)"
    expression4 = "(x + y)/z + 6 + x/z = 3"

    res1 = parse(expression1)
    f_letter, result1 = simplify(res1)
    
    res2 = parse(expression2)
    f_letter, result2 = simplify(res2)

    res3 = parse(expression3)
    f_letter, result3 = simplify(res3)

    res4 = parse(expression4)
    f_letter, result4 = simplify(res4)
    print("\n")
    print(f"Test1: {prettify(res1)}\nResult1: ", prettify(result1))
    print(f"Test2: {prettify(res2)}\nResult2: ", prettify( result2))
    print(f"Test3: {prettify(res3)}\nResult3: ", prettify(result3))
    print(f"Test4: {prettify(res4)}\nResult4: ", prettify(result4))
    print("\n")

    


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
