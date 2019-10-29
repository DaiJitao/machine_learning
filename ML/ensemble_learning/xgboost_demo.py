import numpy as np
from xgboost import XGBClassifier
import xgboost as xgb
import h5py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


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


if __name__ == "__main__":
    X = data = load_competition_data()
    file_label = r"F:\pycharm_workspce\dai_github\machine_learning\data\train_pre_label.csv"
    labels = pd.read_csv(file_label)
    y = labels = labels['label']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)
    print("开始。。。")
    param = {'max_depth': 2, 'eta': 1, 'silent': 1, 'objective': 'binary:logistic'}
    xgb.train()
    clf.fit(X_train, y_train, eval_metric='rmse', verbose=True)
    preds = clf.predict(X_test)
    print(accuracy_score(y_true=y_test, y_pred=preds))
