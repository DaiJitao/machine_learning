"""数据处理和清洗"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

def save_data(data, out_train_file, out_test_file):
    # 查看每一列是否存在null
    # print(call_data.isnull().any())
    train_data = data[data["user"].str.contains("train")]
    test_data = data[data['user'].str.contains("test")]
    print("数据总量：", data)
    print("训练集：", train_data.shape, "测试集：", test_data.shape)
    train_data.to_csv(out_train_file, encoding="utf-8", index=False)
    test_data.to_csv(out_test_file, encoding="utf-8", index=False)
    print("测试集和训练集已经保存-->>", out_train_file, out_test_file)
    return train_data, test_data


def save_all_data():
    all_file2 = "./data/all_data2.csv"
    out_train_file2 = "./data/train_data2.csv"
    out_test_file2 = "./data/test_data2.csv"
    # 通话宽表
    call_file = r"F:\pycharm_workspce\dai_github\myproject\machine_learning\project\ctsi\data\call_data.csv"
    # 个人信息
    cust_file = r"F:\pycharm_workspce\dai_github\myproject\machine_learning\project\ctsi\data\cust_data.csv"
    dpi_file = r"F:\pycharm_workspce\dai_github\myproject\machine_learning\project\ctsi\data\dpi_data.csv"
    # 产品实例信息
    prd_file = r"F:\pycharm_workspce\dai_github\myproject\machine_learning\project\ctsi\data\prd_data.csv"
    # 终端信息
    trmnl_file = r"F:\pycharm_workspce\dai_github\myproject\machine_learning\project\ctsi\data\trmnl_data_update.csv"
    train_file = r"F:\pycharm_workspce\dai_github\myproject\machine_learning\project\ctsi\data\train_result.csv"

    prd_data = pd.read_csv(prd_file, encoding='utf-8')
    call_data = pd.read_csv(call_file, encoding='utf-8')
    cust_data = pd.read_csv(cust_file, encoding='utf-8')
    dpi_data = pd.read_csv(dpi_file, encoding='utf-8')
    trmnl_data = pd.read_csv(trmnl_file, encoding='utf-8')
    train_label = pd.read_csv(train_file, encoding='utf-8')

    all_data = pd.merge(prd_data, call_data, how='left', on='user')
    all_data = pd.merge(all_data, cust_data, how='left', on='user')
    all_data = pd.merge(all_data, dpi_data, how='left', on='user')
    all_data = pd.merge(all_data, trmnl_data, how='left', on='user')
    all_data = pd.merge(all_data, train_label, how='left', on='user')
    all_data.to_csv(all_file2, encoding='utf-8', index=False)
    print("总数据已经保存！", all_file2)
    save_data(all_data, out_train_file=out_train_file2, out_test_file=out_test_file2)

if __name__ == '__main__':
    data_file = r"F:\pycharm_workspce\dai_github\myproject\machine_learning\project\ctsi\data\clean_data\train_data2.csv"
    data = pd.read_csv(data_file)
    print(data.columns)
    #划分数据集X,y
    y = data['label'] # 提取label
    X = data.iloc[:, :-1]


