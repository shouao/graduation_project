from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/predict', methods=['POST'])
def test():
    data = request.get_json()
    repoUrl = data['repoUrl']
    algorithm = data['algorithm']

    # 这里可以根据 repo 和 algorithm 做一些处理，生成测试结果 response

    response = {
        'success': True,
        'files': [
            'test_file_1.txt',
            'test_file_2.txt'
        ],
        'accuracy': 0.6,
        'f1_score': 0.8
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)