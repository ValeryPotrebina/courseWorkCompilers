from parser import parse
from simplify import simplify
from converter import convert, generate_random_numbers
from utils import print_tree, prettify
from flask import Flask, request, jsonify
from flask_cors import CORS
from analyzer import analyze
import  numpy as np
# from solver import solve

app = Flask(__name__)
CORS(app)  # Включаем поддержку CORS
@app.route('/solve', methods=['POST'])
def solve():
    data = request.get_json()
    expression = data.get('expression')
    try:
        result = parse(expression)
        result = simplify(result)
        print_tree(result)
        res = prettify(result)
        print("res", res)
    
        vars, f = convert(result)

        roots, points = analyze(f, vars)

        # for root in roots:
            # print(", ".join([f"{vars[i]} = {root[i]:.6f}" for i in range(len(vars))]) + f", f = {f(root):.6f}")

        # for point in points:
            # print(", ".join([f"{vars[i]} = {point['point'][i]:.6f}" for i in range(len(vars))]) + f", f = {point['value']:.6f}")
        # print("roots: ", roots)

        roots = [root.tolist() if isinstance(root, np.ndarray) else root for root in roots]
        points = [point.tolist() if isinstance(point, np.ndarray) else point for point in points]

        # print("roots: ", roots)
        # print("points: ", points)
        return jsonify({
            'result': str(res),
            'roots': roots,
            'points': points

                        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
# TESTS
# 2*(x-y)^2
# 2*3(x*y)^4
# 2*3(x*y)^4
# y
# /
# x
# 

# 
# sin(x)  ----> Добавить pi в ответ TODO Доработать (-)
# x^3-6*x^2+11*x-6 (+)
# e^x-1  ----->Добавить e, pi (-)
# log(x)(-)
# x^4 - 64 (+) но нет комплексных чисел
# x^2 + y^2 + z^2 - 1

if __name__=="__main__":
    app.run(debug=True)

    # data  = '''
    # x^2
    # '''

    # result = parse(data)
    # result = simplify(result)
    # print_tree(result)
    # print(prettify(result))
    
    # vars, f = convert(result)

    # roots, points = analyze(f, vars)
    


    # for root in roots:
    #     print(", ".join([f"{vars[i]} = {root[i]:.6f}" for i in range(len(vars))]) + f", f = {f(root):.6f}")

    # for point in points:
    #     print(", ".join([f"{vars[i]} = {point['point'][i]:.6f}" for i in range(len(vars))]) + f", f = {point['value']:.6f}")
    # print("roots: ", roots)


    # print("vars: ", vars)
    # print("func: ", func)
    # vars_length = len(vars)
    # args = generate_random_numbers(vars_length)
    # result = func(args)

