from parser.constant import define_constant
from .parser import parser

def parse(data):
    result = parser.parse(data)
    result = define_constant(result)
    return result
