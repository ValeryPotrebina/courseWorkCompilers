from .equal import parse_equal
from .distributivity import distributivity
from .normalize import normalize

def simplify(node):
    f_letter, node = parse_equal(node)
    print(node)
    node = normalize(node)
    node = distributivity(node)
    node = normalize(node)
    return f_letter, node

