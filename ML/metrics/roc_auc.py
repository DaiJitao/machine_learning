import numpy as np
import matplotlib as plt
from itertools import cycle

from sklearn import svm, datasets
from sklearn.metrics import roc_auc_score, auc
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import label_binarize
from sklearn.multiclass import OneVsOneClassifier
from scipy import interp

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


# 打乱数据集并切分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.5,
                                                    random_state=0)

# 学习区分某个类与其他的类
classifier = OneVsRestClassifier(svm.SVC(kernel='linear', probability=True,
                                 random_state=random_state))
y_score = classifier.fit(X_train, y_train).decision_function(X_test)

