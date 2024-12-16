from parser import parse
from simplify import simplify
from converter import convert, generate_random_numbers
from utils import print_tree, prettify
from flask import Flask, request, jsonify
from flask_cors import CORS
from solver import solve

# app = Flask(__name__)
# CORS(app)  # Включаем поддержку CORS
# @app.route('/solve', methods=['POST'])
# def solve():
    # data = request.get_json()
    # expression = data.get('expression')
    # try:
    #     result = parse(expression)
    #     result = simplify(result)
    #     print_tree(result)
    #     res = prettify(result)
    #     print("res", res)
    #     vars, func = convert(result)
    #     vars_length = len(vars)
    #     args = generate_random_numbers(vars_length)
    #     result = func(args)
    #     print(args)
    #     print(result)
    #     out = result
    #     # print(out)
    #     return jsonify({'result': 
    #                     str(res) + "\n" +
    #                     "args: " + str(args) + "\n" +
    #                     str(out) + "\n"})
    # except Exception as e:
    #     return jsonify({'error': str(e)}), 400
    
# TESTS
# 2*(x-y)^2
# 2*3(x*y)^4
# 2*3(x*y)^4
# y
# /
# x
# 

if __name__=="__main__":
    # app.run(debug=True)

    data  = '''
    x^2 + 2*x^2 - 2*x^2 - x - 5 - 1
    '''

    result = parse(data)
    result = simplify(result)
    print_tree(result)
    print(prettify(result))

    vars, func = convert(result)
    roots = solve(func, vars)

    for root in roots:
        print(", ".join([f"{vars[i]} = {root[i]:.6f}" for i in range(len(vars))]) + f", f = {func(root):.6f}")

    # print("roots: ", roots)


    # print("vars: ", vars)
    # print("func: ", func)
    # vars_length = len(vars)
    # args = generate_random_numbers(vars_length)
    # result = func(args)

