import traceback
from parser import parse
from simplify import simplify
from converter import convert
from utils import print_tree, prettify
from flask import Flask, request, jsonify
from flask_cors import CORS
from analyzer import analyze

app = Flask(__name__)
CORS(app)  
@app.route('/api/solve', methods=['POST'])
def solve():
    data = request.get_json()
    expression = data.get('expression')
    try:
        result = parse(expression)
        f_letter, result = simplify(result)
        print(f_letter, prettify(result))
        # print_tree(result)
        res = prettify(result)
        vars, f = convert(result)
        print(vars, f)
        roots, points = analyze(f, f_letter, vars)
        return jsonify({
            'f_letter': f_letter,
            'vars' : vars,
            'result': str(res),
            'roots': roots,
            'points': points

                        })
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 400
    
if __name__=="__main__":
    app.run(debug=True, port=9000)


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
# e^x-1      ----->Добавить e, pi (-)
# log(x)(-)
# x^4 - 64 (+) но нет комплексных чисел
# x^2 + y^2 + z^2 - 1
