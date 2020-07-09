import numpy as np


# 欧式距离
def distEclud(x, y):
    return np.sqrt(np.sum(np.power(x - y, 2)))


# 随机初始化K个质心
def random_center(dataset, K):
    if K < 0:
        return "paramter K={} error!".format(K)
    if dataset:
        examples, features = dataset.shape
        centorids = np.zeros((K, features))
        for i in range(K):
            index = np.random.choice(range(examples))
            centorids[i, :] = dataset[index, :]
        return centorids

def KMeans(dataset, K):
    m = dataset.shape[0]

