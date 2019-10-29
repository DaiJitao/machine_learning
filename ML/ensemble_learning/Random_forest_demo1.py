

'''
数据测试
'''

from sklearn.ensemble import RandomForestClassifier  # 导入随机森林分类器
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import roc_auc_score, accuracy_score
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import matplotlib as mpl
# 导入数据集
from sklearn.datasets import make_regression
import traceback
from sklearn.externals import joblib
import h5py

# 'sepal length', 'sepal width', 'petal length', 'petal width'
iris_feature = u'花萼长度', u'花萼宽度', u'花瓣长度', u'花瓣宽度'

mpl.rcParams['font.sans-serif'] = [u'SimHei']  # 黑体 FangSong/KaiTi
mpl.rcParams['axes.unicode_minus'] = False


def demo2(X, y, n_jobs=1):
    regr = RandomForestRegressor(max_depth=4, random_state=0, n_jobs=n_jobs, )
    regr.fit(X, y)
    print(regr.feature_importances_)
    print(regr.predict([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]))


def load_data(file=None):
    if file == None:
        # 加载声呐数据集
        # 数据说明：
        # 有208行60列特征（值域为0到1），标签为R/M。表示208个观察对象，60个不同角度返回的力度值，二分类结果是岩石/金属。
        file = r"F:\pycharm_workspce\dai_github\machine_learning\data\sonar-all-data.csv"
        data = pd.read_csv(file, header=None)
        X = data.iloc[:, :60].astype(np.float32)
        y = data.iloc[:, 60].astype(np.str)
        # R--> 0 M-->1
        y = y.apply(lambda i: 0 if i == "R" else 1)
        return X, y


def demo3():
    X, y = make_regression(n_samples=100, n_features=10, n_informative=2,
                           random_state=0, shuffle=False)
    X, y = load_data(None)
    clf = RandomForestClassifier(n_estimators=100, max_depth=5, n_jobs=-1)
    clf.fit(X, y)
    y_pred = clf.predict(X)
    y_true = y
    print(accuracy_score(y_true, y_pred))




def load_competition_data(file):
    """
    加载数据：训练集
    :return:
    """
    # file = r"E:\比赛\新建文件夹\train\train_pre_data.h5"

    f = h5py.File(file, mode="r")
    data = f['data']
    res = []
    for i in range(len(data)):
        # 样例数
        exampls = data[i]
        # 灰度数
        grays = np.array(exampls[0])
        # 塑型
        temp = grays.reshape(1, -1)
        res.append(temp[0])

    data_res = np.array(res)
    f.close()
    return data_res


if __name__ == "__main__":

    # 最佳模型
    clf = joblib.load("./models/5clf_model.m")
    # 加载数据
    test_file_a = r"E:\比赛\新建文件夹\test\testa.h5"
    test_file_b = r"E:\比赛\新建文件夹\test\testb.h5"
    X_a = load_competition_data(test_file_a)
    X_b = load_competition_data(test_file_b)
    out_file_a = "./result/submit4.csv"
    out_data = open(out_file_a, mode="w+")
    print(X_a.shape)
    print(X_b.shape)
    y_pred_a = clf.predict(X_a)
    y_pred_b = clf.predict(X_b)
    out_data.write("testa_id,label\n")
    for index, v in enumerate(y_pred_a):
        res = ("testa_%d,%d" %(index, v))
        out_data.write(res)
        out_data.write("\n")
    for index, v in enumerate(y_pred_b):
        res = ("testb_%d,%d" %(index, v))
        out_data.write(res)
        out_data.write("\n")
    out_data.close()