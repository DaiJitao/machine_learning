from sklearn.externals import joblib
from sklearn.svm import SVC
import jieba_fast as jieba
from pyhanlp import HanLP
from gensim.models import Word2Vec
from sklearn.model_selection import train_test_split

import pandas as pd
import numpy as np
from typing import List


def build_sentence_vector(text: List, size: int, imdb_w2v) -> list:
    """
    计算句子的向量：把所有的词相加，取平均值；
    :param text: 文本分词之后的句子
    :param size: 词向量的维度（512）
    :param imdb_w2v: 词向量模型
    :return:
    """
    vec = np.zeros(size).reshape((1, size))
    count = 0.
    for word in text:
        try:
            temp = imdb_w2v[word] if word in imdb_w2v else np.array([0] * size)
            vec += temp.reshape((1, size))
            count += 1.
        except KeyError:
            continue
    if count != 0:
        vec /= count
    return vec


allVec = "./data/mergedVector.npy"
isConvert = False  # 文本是否转换为词向量
if isConvert:
    # 加载词向量模型
    model_file = "./models/gensim_CBOW_w2v.model"
    model = Word2Vec.load(model_file)
    print("北京" in model)
    # 加载文本
    negfile = "./data/negCutWords.csv"
    posfile = "./data/posCutWords.csv"
    result = []
    with open(negfile, encoding='utf-8') as fp:
        lines = fp.readlines()
        for line in lines[1:]:
            temps = line.strip().split(",")
            text = temps[0].split(" ")
            sentVector = build_sentence_vector(text, 512, model)  # shape:(1,512)
            label = 0
            sentVectorLabel = [sentVector, label]
            result.append(sentVectorLabel)

    with open(posfile, encoding='utf-8') as fp:
        lines = fp.readlines()
        for line in lines[1:]:
            temps = line.strip().split(",")
            text = temps[0].split(" ")
            sentVector = build_sentence_vector(text, 512, model)  # shape:(1,512)
            label = 1
            sentVectorLabel = [sentVector, label]
            result.append(sentVectorLabel)

    np.random.shuffle(result)
    np.save(allVec, result)

xx = 10
data_x = "./data/data_x.npy"
label_y = "./data/label_y.npy"
isSplit = False  # 拆分x和y
if isSplit:
    result = np.load(allVec)
    data = []
    label = []
    for e in result:
        X = e[0]
        y = e[1]
        label.append(y)
        data.append(X)
    data = np.array(data)
    label = np.array(label)
    np.save(data_x, data)
    np.save(label_y, label)

if __name__ == '__main__':
    isTrain = True # 是否训练模型
    isTest = False
    allVec = "./data/mergedVector.npy"
    x = np.load(data_x)
    y = np.load(label_y)
    x = x.reshape((-1, 512))
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.1, random_state=42)
    base = './models/'
    if isTrain:
        kernels = ['sigmoid', 'precomputed']
        degrees = range(2,10)
        re = []
        for kernel in kernels:
            for d in degrees:
                if kernel == 'poly':
                    clf = SVC(kernel=kernel, verbose=True, degree=d)
                    clf.fit(X_train, y_train)
                    svmModel = base + kernel + "_degree_" + str(d) + "model.pkl"
                    joblib.dump(clf, svmModel)
                    print(svmModel, clf.score(X_test, y_test))
                else:
                    if kernel not in re:
                        clf = SVC(kernel=kernel, verbose=True)
                        clf.fit(X_train, y_train)
                        svmModel = base + "svm_" + kernel + "_model.pkl"
                        joblib.dump(clf, svmModel)
                        print(svmModel, clf.score(X_test, y_test))
                        re.append(kernel)

    if isTest:
        model = joblib.load(svmModel)
        print(model.score(X_test, y_test))