

''''
根据李航统计学方法编写
'''
import pandas as pd
from collections import Counter
import numpy as np

def create_data():
    datasets = [['青年', '否', '否', '一般', '否'],
               ['青年', '否', '否', '好', '否'],
               ['青年', '是', '否', '好', '是'],
               ['青年', '是', '是', '一般', '是'],
               ['青年', '否', '否', '一般', '否'],
               ['中年', '否', '否', '一般', '否'],
               ['中年', '否', '否', '好', '否'],
               ['中年', '是', '是', '好', '是'],
               ['中年', '否', '是', '非常好', '是'],
               ['中年', '否', '是', '非常好', '是'],
               ['老年', '否', '是', '非常好', '是'],
               ['老年', '否', '是', '好', '是'],
               ['老年', '是', '否', '好', '是'],
               ['老年', '是', '否', '非常好', '是'],
               ['老年', '否', '否', '一般', '否'],
               ]
    labels = [u'年龄', u'有工作', u'有自己的房子', u'信贷情况', u'类别']
    # 返回数据集和每个维度的名称
    return datasets, labels

def loadData():
    """加载数据

    """
    datasets, labels = create_data()
    dataDF = pd.DataFrame(data=datasets, columns=labels)
    return dataDF


def calc_entroy(data):
    '''
    计算信息熵
    :param data:
    :return: float
    '''
    # 信息熵
    length, cols = data.shape
    if length == 0 or cols == 0:
        return 0.0
    labels = data.iloc[:, -1]
    c = Counter(labels)
    entroy = 0.0
    for key, v in c.items():
        p = (v / length)  # 概率
        entroy += (-p * np.log2(p))
    return entroy

# 计算条件熵
def calc_condi_entroy(data, feature):
    '''
    计算信息熵
    :param data:
    :param feature:指定特征下标,None计算素有特征
    :return: float
    '''
    # 信息熵
    length, cols = data.shape
    if length == 0 or cols == 0:
        return 0.0
    # 一共有（cols-1）个特征
    dataDF = data.iloc[:, feature]
    c = Counter(dataDF)
    condi_entropy = 0.0
    for key, value in c.items():
        temp = data.loc[data.iloc[:, feature]==key] # 划分数据集
        split_data = temp.iloc[:, [-1]]
        entropy = calc_entroy(split_data)
        p = (value/length)
        condi_entropy += p * entropy
    return condi_entropy

def splited_feature(data):
    """
    计算每个特征的条件熵
    :param data:
    :return: []
    """
    entropy = calc_entroy(data)
    size, feature_size = data.shape
    cols_names = data.columns
    history = [] # 存放计算历史
    for i in range(feature_size-1):
        condi_entropy = calc_condi_entroy(data, feature=i)
        gain = entropy - condi_entropy
        name = cols_names[i]
        history.append((i, gain, name))
    return history
def get_best_feature(data):
    """
    获取最佳特征
    :param data:
    :return:
    """
    history = splited_feature(data)
    res = max(history, key=lambda x: x[-1])
    return res

class BinayTree(object):
    def __init__(self, feature_name, feature, gain, label, data):
        self.next = None
        self.name = feature_name
        self.value = gain
        self.feature = feature
        self.label = label # 类型
        self.data = data
        self.result = {'label:': self.label, 'feature': self.feature, 'tree': self.tree}

    def __repr__(self):
        return '{}'.format(self.result)


if __name__ == "__main__":
    data = pd.DataFrame
    data = loadData()





