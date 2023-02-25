from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/predict', methods=['POST'])
def test():
    data = request.get_json()
    repo = data['repo']
    algorithm = data['algorithm']

    # 这里可以根据 repo 和 algorithm 做一些处理，生成测试结果 response

    response = {
        'success': True,
        'data': {
            'files': [
                'test_file_1.txt',
                'test_file_2.txt'
            ],
            'accuracy': 0.6,
            'f1-score': 0.8
        }
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)