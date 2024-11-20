from .distributivity import distributivity
from .normalize import normalize

def simplify(node):
    node = distributivity(node)
    # print("distributivity: ", node)
    node = normalize(node)
    # print("normalize: ", node)
    return node