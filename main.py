from parser import parse, print_tree, prettify
from calc import calc

if __name__=="__main__":
    # 

    data  = '''
    - (z * (x - y))
    '''

    # (2 * (y + z))*x -> (2y + 2z)x = 2yx + 2xz
    # (2 * (y + z))*(x + 5) -> (2yx + 2xz)(x + 5) -> ?
    # ((x + y) + z)(a + b) ?
    # (a + b)*(c + d) -> (a+b)c + (a+b)d
    # - (z * (x - y)) ->  (zx - zy) 

    result = parse(data)
    print_tree(result)
    print(prettify(result))

    result = calc(result)
    print_tree(result)
    print(prettify(result))
