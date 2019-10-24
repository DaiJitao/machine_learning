
import numpy as np
import pandas as pd

# 导入csv文件
def loadDataSet(filename):
    dataset = []
    with open(filename, 'r') as fr:
        for line in fr.readlines():
            if not line:
                continue
            lineArr = []
            for featrue in line.split(','):
                # strip()返回移除字符串头尾指定的字符生成的新字符串
                str_f = featrue.strip()
                if str_f.isdigit(): # 判断是否是数字
                    # 将数据集的第column列转换成float形式
                    lineArr.append(float(str_f))
                else:
                    # 添加分类标签
                    lineArr.append(str_f)
            dataset.append(lineArr)
    return dataset

class CartTree(object):
    def __init__(self):
        pass

    def _init_args(self):
        pass

    def _gini(self,):
        pass

if __name__ == "__main__":
    file = r"F:\pycharm_workspce\dai_github\machine_learning\data\sonar-all-data.txt"
    file = r"F:\pycharm_workspce\dai_github\machine_learning\data\sonar-all-data.csv"
    from random import randrange
