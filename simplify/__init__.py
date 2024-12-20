from .compare import parse_equal
from .distributivity import distributivity
from .normalize import normalize

def simplify(node):
    print("1", node)
    node = parse_equal(node)
    print("2",node)
    node = normalize(node)
    print("3",node)
    node = distributivity(node)
    print("4", node)
    # print("distributivity: ", node)
    node = normalize(node)
    print("5", node)
    # print("normalize: ", node)
    return node

