import numpy as np
import matplotlib.pyplot as plt
from itertools import cycle
import pandas as pd

from sklearn import svm, datasets
from sklearn.metrics import roc_auc_score, auc, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import label_binarize
from sklearn.multiclass import OneVsOneClassifier
from scipy import interp
import random
import matplotlib as mpl

mpl.rcParams['font.sans-serif'] = ['KaiTi']
mpl.rcParams['font.serif'] = ['KaiTi']

# 导入数据
iris = datasets.load_iris()
X = iris.data
y = iris.target
print(y)
# 二值化输出
y = label_binarize(y, classes=[0, 1, 2])
print(y)

# 二进制化输出
y = label_binarize(y, classes=[0, 1, 2])  # shape==(150, 3)
n_classes = y.shape[1]  # n_classes==3

# 添加噪音特征，使问题更困难
random_state = np.random.RandomState(0)
n_samples, n_features = X.shape  # n_samples==150, n_features==4
X = np.c_[X, random_state.randn(n_samples, 200 * n_features)]  # shape==(150, 84)


def roc_plot():
    pass


def select(i):
    if i % 5 == 0:
        y = -10
    elif i % 5 == 1:
        y = -20
    elif i % 5 == 2:
        y = -30
    elif i % 5 == 3:
        y = 30
    elif i % 5 == 4:
        y = 20
    else:
        y = 10
    return y


if __name__ == "__main__":
    csv = r"F:\pycharm_workspce\dai_github\machine_learning\ML\metrics\data\data.csv"
    data = pd.read_csv(csv)
    size = data.shape[0]
    step = 1 / size

    y_true = data['cls']
    y_pred = data['p']
    y_true = list(map(lambda x: 1.0 if x == 'p' else 0.0, y_true))
    threshold = 1.0
    false_ratios = []  # 假阳率
    true_ratios = []  # 真阳率
    ticks = []
    while threshold >= 0.0:
        temp = y_pred.copy(deep=True)
        temp[temp <= threshold] = 0.0
        temp[temp > threshold] = 1.0
        d = confusion_matrix(y_true=y_true, y_pred=temp)
        tn, fp, fn, tp = d.ravel()
        false_ratios.append(fp / (fp + tn))
        true_ratios.append(tp / (tp + fn))
        ticks.append(threshold)
        threshold = threshold - step

    ticks.append(0.0)
    ticks.sort()
    print(false_ratios)
    print(true_ratios)

    plt.plot(false_ratios, true_ratios, '-o')
    i = 0
    for xy in zip(false_ratios, true_ratios):
        # plt.annotate("坐标值={}\n概率={}".format((xy), y_pred[i]), xy=xy, xytext=(-20, 10), textcoords='offset points', weight='heavy')
        if i % 3 == 0:
            x = -100
        elif i % 3 == 1:
            x = 60
        else:
            x = -60
        y = select(i)
        plt.annotate("p:{}".format(y_pred[i]), xy=xy, textcoords='offset points',
                     xytext=(x, y),
                     arrowprops=dict(arrowstyle='-|>', connectionstyle='arc3', color='red'),
                     bbox=dict(boxstyle='round,pad=0.5', fc='yellow', ec='k', lw=1, alpha=0.4))
        i += 1
    plt.grid(True)
    plt.xticks(ticks)
    plt.yticks(ticks)
    plt.show()
