from parser import parse, print_tree
from calc import calc

if __name__=="__main__":
    # 

    data  = '''
    sin(1.434343425)^2 + cos(1.434343425)^2
    '''

    result = parse(data)
    print_tree(result)

    result = calc(result)
    print(result)