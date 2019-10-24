

"""
决策树常用的工具类：指标的计算、数据的加载

"""



import numpy as np

def load_data():
    '''
    根据《统计学习方法》第八章8.1.3产生数据.
    :return:
    '''
    dataset_label = np.array([[0, 1], [1, 1], [2, 1], [3, -1], [4, -1], [5, -1], [6, 1], [7, 1], [8, 1], [9, -1]])
    return dataset_label

