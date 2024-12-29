from parser.constant import define_constant
from utils import print_tree
from .parser import parser

def parse(data):
    result = parser.parse(data)
    result = define_constant(result)
    print_tree(result)
    return result
