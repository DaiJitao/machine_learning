from sklearn.ensemble import RandomForestClassifier  # 导入随机森林分类器
from sklearn.metrics import roc_auc_score, accuracy_score
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import matplotlib as mpl

# 'sepal length', 'sepal width', 'petal length', 'petal width'
iris_feature = u'花萼长度', u'花萼宽度', u'花瓣长度', u'花瓣宽度'


def iris_type(s):
    it = {'Iris-setosa': 0, 'Iris-versicolor': 1, 'Iris-virginica': 2}
    return it[s]


def transfer(y):
    d = np.array([iris_type(s) for s in y])
    return d


def vote(y):
    pass


mpl.rcParams['font.sans-serif'] = [u'SimHei']  # 黑体 FangSong/KaiTi
mpl.rcParams['axes.unicode_minus'] = False

if __name__ == "__main__":
    # model = RandomForestClassifier(n_estimators=100, bootstrap=True, max_features='sqrt')
    iris = r"F:\pycharm_workspce\dai_github\machine_learning\data\iris.data"
    df = pd.read_csv(iris, header=None)
    x, y = df.iloc[:, :4], df.iloc[:, 4]
    feature_pairs = [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]]
    # 随机森林
    clf = RandomForestClassifier(n_estimators=200, criterion='entropy', max_depth=4)
    y = transfer(y)  # 数据转换
    # y = y.reshape(-1, 1)
    # print(y.shape)
    # 全部特征值 训练模型
    rf_clf = clf.fit(x, y)
    # 准确率
    y_pre = rf_clf.predict(x)
    y_pres = []  # 保存预测结果
    print("整体特征-随机森林预测结果", y_pre)
    acc = accuracy_score(y, y_pre)
    print("整体特征-随机森林预测结果准确率", acc)
    # 特征选取
    feature_pairs = [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3], [0, 1, 2], [1, 2, 3], [0, 2, 3], [0, 1, 3],
                     [0, 1, 2, 3]]

    clfs = []
    for pairs in feature_pairs:
        x_t = x.iloc[:, pairs]
        rf_clf = clf.fit(x_t, y) # 如果训练的维度是2，预测的时候维度也必须是2；维度保持一致
        y_pre = rf_clf.predict(x_t)
        acc = accuracy_score(y, y_pre)
        print(pairs, "-随机森林预测结果准确率", acc)
        y_pres.append(y_pre)
        clfs.append(rf_clf)
