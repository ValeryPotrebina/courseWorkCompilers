from parser import parse, print_tree, prettify
from calc import calc
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
        print_tree(result)
        print(prettify(result))
        out = prettify(calc(result))
        print(out)
        return jsonify({'result': str(out)})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    

if __name__=="__main__":
    app.run(debug=True)

    # data  = '''
    # - (z * (x - y))
    # '''

    # (2 * (y + z))*x -> (2y + 2z)x = 2yx + 2xz
    # (2 * (y + z))*(x + 5) -> (2yx + 2xz)(x + 5) -> ?
    # ((x + y) + z)(a + b) ?
    # (a + b)*(c + d) -> (a+b)c + (a+b)d
    # - (z * (x - y)) ->  (zx - zy) 

    # result = parse(data)
    # print_tree(result)
    # print(prettify(result))

    # result = calc(result)
    # print_tree(result)
    # print(prettify(result))
