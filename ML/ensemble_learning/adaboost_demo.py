import numpy as np
import matplotlib.pyplot as plt


def load_data():
    '''
    根据《统计学习方法》第八章8.1.3产生数据.
    :return:
    '''
    dataset_label = np.array([[0, 1], [1, 1], [2, 1], [3, -1], [4, -1], [5, -1], [6, 1], [7, 1], [8, 1], [9, -1]])
    return dataset_label


def __error_rate(dataset: list, labels: list, classifier) -> float:
    '''

    :param dataset:
    :param labels:
    :param classifier:
    :return:
    '''
    if classifier == None:
        raise Exception("classifier != None")
    sample_size = len(dataset)
    if sample_size == 0:
        raise Exception("dataset can not be empty!")
    error_count = 0

    for x, y in zip(dataset, labels):
        if classifier(x) != y:
            error_count += 1

    return error_count / sample_size


def __classifier(x, threshold=2.5):
    if x == None:
        raise Exception("x != None")
    if threshold == None:
        threshold = 0.0
    return 1 if x <= 2.5 else -1


class Adaboost(object):
    def __init__(self):
        pass

    def __init_args(self, dataset, labels):
        '''

        :param data: np.array
        :param labels: np.array
        :return:
        '''
        self.sample_size, self.feature_size = dataset.shape
        self.weights = [1.0 / self.sample_size] * self.sample_size
        self.dataset = dataset
        self.labels = labels
        self.classifiers = []

    def __get_alpha(self, error_rate):
        '''
        计算阿尔法值
        :param error_rate:
        :return:
        '''
        if error_rate <= 0:
            raise Exception(" error_rate <= 0 error!")
        temp = (1 - error_rate) / error_rate
        return 0.5 * np.log2(temp)

    def __error_rate(self, weights, classifier):
        if weights == None or len(weights) == 0:
            raise Exception("weights == None or len(weights) == 0 error!")

        error_rate = 0.0
        for w, x, y in zip(weights, self.dataset, self.labels):
            if classifier(x) != y:
                error_rate += w
        return error_rate

    def __normalization_factor(self, weights, alpha, classifier):
        z = 0
        for w, x, y in zip(weights, self.dataset, self.labels):
            z += (w * np.exp(-1 * alpha * y * classifier(x)))
        return z

    def __update_weights(self, weights, z, alpha, classifier):
        '''
        更新权重值
        :param weights:
        :param z:
        :param alpha:
        :param classifier:
        :return:
        '''
        w = [(weights[i] * np.exp(-1 * alpha * self.labels[i] * classifier(self.dataset[i])) / z) for i in
             range(self.sample_size)]
        return w


def a1(e):
    if e == 0 or e == None:
        raise Exception("输入参数有误！")
    t = float((1 - e) / e)
    res = .5 * np.log2(t)
    return res


if __name__ == "__main__":
    pass
