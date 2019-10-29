from timeit import timeit
import time
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


def demo1():
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
        rf_clf = clf.fit(x_t, y)  # 如果训练的维度是2，预测的时候维度也必须是2；维度保持一致
        y_pre = rf_clf.predict(x_t)
        acc = accuracy_score(y, y_pre)
        print(pairs, "-随机森林预测结果准确率", acc)
        y_pres.append(y_pre)
        clfs.append(rf_clf)


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


import h5py


# import h5py._hl.dataset.Dataset


def load_competition_data():
    """
    加载数据：训练集
    :return:
    """
    file = r"E:\比赛\新建文件夹\train\train_pre_data.h5"
    file_label = r"F:\pycharm_workspce\dai_github\machine_learning\data\train_pre_label.csv"
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


def load_competition_test_data():
    '''
    加载数据：测试集
    :return:
    '''
    file = r"E:\比赛\新建文件夹\train\testa.h5"
    file_label = r"F:\pycharm_workspce\dai_github\machine_learning\data\train_pre_label.csv"
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


def find_best_args():
    """
    寻找最佳参数
    :return:
    """
    outfile = "./result_rf.csv"
    outdata = open(outfile, mode="w+", encoding="utf-8")
    outdata.write("n_estor,max_dph,min_spls_leaf,acc\n")
    count = 1
    min_ = .0
    if None:
        n_estimators = [100, 200, 500, 600, 1000, 1500]
        max_depthes = range(2, 10)
        min_samples_leafs = range(1, 90)
        # 寻找随机森林最佳参数
        for n_estimator in n_estimators:
            for max_depth in max_depthes:
                for min_samples_leaf in min_samples_leafs:
                    clf = RandomForestClassifier(n_estimators=n_estimator, max_depth=max_depth, n_jobs=-1,
                                                 min_samples_leaf=min_samples_leaf)
                    clf.fit(X_train, y_train)
                    y_pred = clf.predict(X_test)
                    acc = accuracy_score(y_true=y_test, y_pred=y_pred)
                    rs = ("%d,%d,%d,%f" % (n_estimator, max_depth, min_samples_leaf, acc))
                    if acc > min_:
                        min_ = acc
                    outdata.write(rs)
                    outdata.write("\n")
                    count += 1
                    if count % 50 == 0:
                        print("...")
                        outdata.flush()
        outdata.write("last=" + str(min_))
    outdata.close()
    print("训练完毕！")


def best_args_model(outfile, X_train, X_test, y_train, y_test):
    '''
    训练最佳参数
    :param outfile:
    :param X_train:
    :param X_test:
    :param y_train:
    :param y_test:
    :return:
    '''
    outdata = open(outfile, mode="w+", encoding="utf-8")
    outdata.write("n_estor,max_dph,min_spls_leaf,acc\n")
    n_estimators = [100, 200, 600, 1000, 1500, 2000]
    max_depthes = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
    min_samples_leafs = [43, 7, 6, 5, 4, 3, 2]
    count = 0
    max_acc = 0.9666
    try:
        for n_estimator in n_estimators:
            for max_depth in max_depthes:
                for min_samples_leaf in min_samples_leafs:
                    # 最佳参数:训练5次
                    for i in range(20):
                        clf = RandomForestClassifier(n_estimators=n_estimator, max_depth=max_depth, n_jobs=-1,
                                                     min_samples_leaf=min_samples_leaf)
                        clf.fit(X_train, y_train)
                        y_pred = clf.predict(X_test)
                        acc = accuracy_score(y_true=y_test, y_pred=y_pred)
                        rs = ("%d,%d,%d,%f" % (n_estimator, max_depth, min_samples_leaf, acc))
                        outdata.write(rs)
                        outdata.write("\n")
                        count += 1
                        if count % 10 == 0:
                            print(count, "writed in ...")
                            outdata.flush()
                        if acc - max_acc > 0.0:
                            max_acc = acc
                            joblib.dump(clf, "./models/" + str(count) + "clf_model.m")
                            print("./models/" + str(count) + "clf_model.m")
                            print(rs, "acc: ", acc)

        outdata.close()
        print("训练完毕！")
    except Exception as e:
        outdata.close()
        traceback.print_exception(e)


if __name__ == "__main__":
    X = data = load_competition_data()
    file_label = r"F:\pycharm_workspce\dai_github\machine_learning\data\train_pre_label.csv"
    labels = pd.read_csv(file_label)
    y = labels = labels['label']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

    best_args_model("./result/best_args_res.csv", X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test)
    # 最佳参数
    # n_estimator = 2000
    # max_depth = 20
    # min_samples_leaf = 2
    # max_acc = 0.966
    # for i in range(1000):
    #     clf = RandomForestClassifier(n_estimators=n_estimator, max_depth=max_depth, n_jobs=-1,
    #                                  min_samples_leaf=min_samples_leaf)
    #     clf.fit(X_train, y_train)
    #     y_pred = clf.predict(X_test)
    #     acc = accuracy_score(y_true=y_test, y_pred=y_pred)
    #     rs = ("%d,%d,%d,%f" % (n_estimator, max_depth, min_samples_leaf, acc))
    #     print(rs)
    #     if True: # acc - max_acc > 0.0:
    #         # max_acc = acc
    #         joblib.dump(clf, "./models/" + str(i) + "clf_model.m")
    #         print("./models/" + str(i) + "clf_model.m")
