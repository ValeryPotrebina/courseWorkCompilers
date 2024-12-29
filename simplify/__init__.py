from utils import prettify
from .equal import parse_equal
from .distributivity import distributivity
from .normalize import normalize

def simplify(node):
    f_letter, node = parse_equal(node)
    print(node)
    node = normalize(node)
    print("normalize: ", prettify(node))
    node = distributivity(node)
    print("dist: ", prettify(node))
    node = normalize(node)
    print("normalize: ", prettify(node))
    return f_letter, node

