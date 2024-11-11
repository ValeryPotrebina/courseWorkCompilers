from parser import parse, print_tree, prettify
from calc import calc
from simplify.simplify import simplify, getOperands, normalizeMult
# from flask import Flask, request, jsonify
# from flask_cors import CORS


# app = Flask(__name__)
# CORS(app)  # Включаем поддержку CORS

# @app.route('/solve', methods=['POST'])
# def solve():
#     data = request.get_json()
#     expression = data.get('expression')

#     try:
#         result = parse(expression)
#         print_tree(result)
#         print(prettify(result))
#         out = prettify(calc(result))
#         print(out)
#         return jsonify({'result': str(out)})
#     except Exception as e:
#         return jsonify({'error': str(e)}), 400

# TESTS
# 2*(x-y)^2
# 2*3(x*y)^4
# 2*3(x*y)^4
if __name__=="__main__":
    # app.run(debug=True)


# TODO: 2*(x*y)*(x*y)^2

    data  = '''
         x*y + x*y
    '''
    # 2 * (3 * b)

# BiOp(Num(6) * BiOp(x * BiOp(x * Num(3))))


# 2(x-y)(x-y)
# 2(xx-xy-yx+yy)=2xx-2xy-2yx+2yy
    # -(zx - zy) -> -zx + zy

    # (2 * (y + z))*x -> (2y + 2z)x = 2yx + 2xz
    # (2 * (y + z))*(x + 5) -> (2yx + 2xz)(x + 5) -> ?
    # ((x + y) + z)(a + b) ?
    # (a + b)*(c + d) -> (a+b)c + (a+b)d
    # - (z * (x - y)) ->  (zx - zy) 

    result = parse(data)
    print(prettify(simplify(result)))

    # result = calc(result)
    # print_tree(result)
    # print(prettify(result))
