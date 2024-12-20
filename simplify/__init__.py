from .equal import parse_equal
from .distributivity import distributivity
from .normalize import normalize

def simplify(node):
    # print("1", node)
    f_letter, node = parse_equal(node)
    # print("2",node)
    node = normalize(node)
    # print("3",node)
    node = distributivity(node)
    # print("4", node)
    node = normalize(node)
    # print("5", node)
    return f_letter,node

