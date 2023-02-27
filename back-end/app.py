from flask import Flask, request, jsonify
from flask_cors import CORS
import git
import os

import numpy as np  
from sklearn import linear_model, datasets
from sklearn.model_selection import train_test_split 
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
CORS(app)

def is_bugfix(message):
    keywords = ['bug', 'fix', 'patch', 'issue']
    message = message.upper()
    for keyword in keywords:
        if keyword.upper() in message:
            return True
    return False

def keyword_count(content, keyword):
    index = content.find(keyword)
    count = 0
    while index != -1:
        count += 1
        index = content.find(keyword, index + 1)
    return count

def feature_extract(fileName):
    features = [0] * 7
    lines = ''
    with open(fileName, 'r') as f:
	    lines = f.readlines()
    
    features[0] += (len(lines))
    for line in lines:
        features[1] += (keyword_count(line, 'for') + keyword_count(line, 'while')) # for while
        features[2] += (keyword_count(line, 'if')) # if 
        features[3] += (keyword_count(line, 'else')) # else
        features[4] += (keyword_count(line, 'import') + keyword_count(line, 'include')) # import include
        features[5] += (keyword_count(line, 'class')) # class
        features[6] += (keyword_count(line, '#') + keyword_count(line, '/*') + keyword_count(line, '//')) # # /* */ //
    return features

def liner_regression(features, lables):
    X = features
    y = lables
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
    
    sc = StandardScaler()
    sc.fit(X_train)
    X_train_std = sc.transform(X_train)
    X_test_std = sc.transform(X_test)
    
    # 训练逻辑回归模型
    logreg = linear_model.LogisticRegression(C=1e5)
    logreg.fit(X_train, y_train)
    
    prepro = logreg.predict_proba(X_test_std)
    acc = logreg.score(X_test_std, y_test)
    return acc

def repo_poller(url):
    repoName = url.split('/')[-1].split('.')[0]
    git.Repo.clone_from(url, f'./.repo/{repoName}')
    repo = git.Repo(f'./.repo/{repoName}')
    commits = [commit for commit in repo.iter_commits()]
    choosePoint = commits[len(commits) // 2]
    g = repo.git
    g.checkout(choosePoint.hexsha)
    fileList = g.ls_files().split('\n')
    fileList = [File for File in fileList if File.endswith('.c') or File.endswith('.cpp') or File.endswith('.java') or File.endswith('.go')]
    os.system(f"cd ./.repo/{repoName} && git checkout {choosePoint.hexsha}")
    
    features = []
    for File in fileList:
        features.append(feature_extract(f'./.repo/{repoName}/' + File))

    bugRate = {}

    for commit in commits:
        if is_bugfix(commit.message):
            effectedFiles = [File for File in commit.stats.files.keys()]
            for File in effectedFiles:
                if (File in bugRate):
                    bugRate[File] += 1
                else:
                    bugRate[File] = 0
    brs = []
    
    for File in fileList:
        if (File in bugRate):
            brs.append(bugRate[File])
        else:
            brs.append(0)
    
    brs.sort()
    pivot = brs[-(len(brs) // 5)]
    lables = []
    
    for File in fileList:
        if (File in bugRate and bugRate[File] > pivot):
            lables.append(1)
        else:
            lables.append(0)
    
    return fileList, liner_regression(features, lables)
    

@app.route('/api/predict', methods=['POST'])
def test():
    os.system(f'rm ./.repo -rf')
    data = request.get_json()
    repoUrl = data['repoUrl']
    algorithm = data['algorithm']

    fileList, acc = repo_poller(repoUrl)
    # 这里根据 repo 和 algorithm 做一些处理，生成测试结果 response

    response = {
        'success': True,
        'files': fileList,
        'accuracy': acc
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)