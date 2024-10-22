from parser import parse, print_tree
from calc import calc

if __name__=="__main__":
    # 

    data  = '''
    5 + 3 * 7 * (x + 4)
    '''

    result = parse(data)
    print_tree(result)

    result = calc(result)
    print_tree(result)