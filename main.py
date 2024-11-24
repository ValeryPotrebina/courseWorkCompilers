from parser import parse
from simplify import simplify
from converter import convert, generate_random_numbers
from utils import print_tree, prettify
from flask import Flask, request, jsonify
from flask_cors import CORS


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
        vars, func = convert(result)
        vars_length = len(vars)
        args = generate_random_numbers(vars_length)
        result = func(args)
        print(args)
        print(result)
        out = result
        # print(out)
        return jsonify({'result': 
                        str(res) + "\n" +
                        "args: " + str(args) + "\n" +
                        str(out) + "\n"})
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
if __name__=="__main__":
     app.run(debug=True)

#     data  = '''
#         x / (y / z)
#     '''

#     result = parse(data)
#     result = simplify(result)
#     print_tree(result)
#     print(prettify(result))

    # vars, func = convert(result)
    # vars_length = len(vars)
    # args = generate_random_numbers(vars_length)
    # result = func(args)
    # print(args)
    # print(result)  # Вывод: sin(1) + 2 * 2

#     # operands = getOperands(result, "+")
#     # print("operands (main): ", operands)



# '''
# 1. Решить уравнение
# 2. Вывести график
# 3. Сервак подрубить 
# '''

# 
# 