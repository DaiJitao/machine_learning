import numpy as np
import matplotlib.pyplot as plt
# from sklearn import cross_validation
from sklearn.svm import SVC # 分类模型
from sklearn.svm import SVR # 回归模型
from sklearn.model_selection import train_test_split
# from ML.svm.utilities import plot_classifier
import threading
from sklearn.metrics import classification_report
from sklearn.preprocessing import label_binarize, LabelEncoder


def load_data(file):
    X, y = [], []
    with open(file, mode='r') as f:
        for line in f.readlines():
            data = [float(x) for x in line.split(",")]
            X.append(data[:-1])
            y.append(data[-1])
    return np.array(X), np.array(y)


def plot(file=None):
    file = "./data/data_multivar.txt"
    X, y = load_data(file)

    class_0 = np.array([X[i] for i in range(len(X)) if y[i] == 0])
    class_1 = np.array([X[i] for i in range(len(X)) if y[i] == 1])

    plt.figure()
    clrs = ['red', 'green', "None"]
    plt.scatter(class_0[:, 0], class_0[:, 1], facecolors=clrs[0], edgecolors=clrs[0],
                marker='s')
    plt.scatter(class_1[:, 0], class_1[:, 1], facecolors=clrs[1], edgecolors=clrs[1],
                marker='s')
    plt.title('Input data')
    plt.show()


def train_model(params, file=None):
    '''
    # 分割数据集并用SVM训练模型
    :return:
    '''
    file = "./data/data_multivar.txt"
    X, y = load_data(file)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=5)
    # params = {'kernel': p[0]}
    classifier = SVC(**params)
    classifier.fit(X_train, y_train)
    # plot_classifier(classifier, X_train, y_train, 'Training dataset')
    plt.show()


def model(params, file=None):
    '''
    # 分割数据集并用SVM训练模型
    :return:
    '''
    file = "./data/data_multivar.txt"
    X, y = load_data(file)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=5)
    classifier = SVC(**params)
    classifier.fit(X_train, y_train)
    # plot_classifier(classifier, X_test, y_test, 'Test dataset')
    plt.show()

def report(params):
    file = "./data/data_multivar.txt"
    X, y = load_data(file)
    # 划分测试集和训练集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=5)
    classifier = SVC(**params)
    classifier.fit(X_train, y_train)

    target_names = ['Class-' + str(int(i)) for i in set(y)]
    print("\n" + "#" * 60)
    print("\nClassifier performance on training dataset\n")
    print(classification_report(y_train, classifier.predict(X_train)))
    print("#" * 60 + "\n")

if __name__ == "__main__":
    p = ["rbf", "linear", "poly", "sigmoid", "precomputed"]
    # 用了一个三次多项式方程
    params = {'kernel': 'poly', 'degree': 3}
    #train_model(params)
    #test_model(params)
    report(params)
    d = ["a", "a", "b", "c", "c"]
    print(label_binarize(d, classes=["a", "b", "c"]))
    le = LabelEncoder()
    le.fit(d)
    print(le.classes_)



