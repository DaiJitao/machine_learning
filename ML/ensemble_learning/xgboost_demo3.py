from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

import pandas as pd
import matplotlib.pyplot as plt
import os
import xgboost as xgb
import warnings
warnings.filterwarnings('ignore')
os.environ['PATH'] += os.pathsep + r'E:\Program Files (x86)\Graphviz2.38\bin'

'''

xgboost实例：https://zhuanlan.zhihu.com/p/83620830
可视化安装方法： https://blog.csdn.net/qq_20090041/article/details/89675373?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromBaidu-1&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromBaidu-1
'''

boston = datasets.load_boston()
def load_data():
    '''
    # 加载数据集 波斯顿房价数据集
    :return:
    '''
    data = pd.DataFrame(boston.data)
    data.columns = boston.feature_names
    return data, boston.target


# 数据集转换：因为dmatrix 格式 在xgboost当中运行速度更快，性能更好。
X, y = load_data()


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

for epoch in range(3,10):
    # 随机选取默认参数进行初始化建模
    xg_reg = xgb.XGBRegressor(objective='reg:linear', colsample_bytree=0.3, learning_rate=0.1, max_depth=epoch,
                              n_estimators=10, alpha=10)

    xg_reg.fit(X_train, y_train)
    y_pred = xg_reg.predict(X_test)
    print("参数max_depth={0}, {1}".format(epoch, mean_squared_error(y_test, y_pred)))

data,y = load_data()
data['price'] = y
data_matrix = xgb.DMatrix(data, y)

params = {"objective":"reg:linear",'colsample_bytree': 0.3,'learning_rate': 0.1,
                'max_depth': 5, 'alpha': 10}
cv_results = xgb.cv(dtrain=data_matrix, params=params, nfold=3,
                    num_boost_round=50,early_stopping_rounds=10,metrics="rmse", as_pandas=True, seed=123)
print(cv_results.head())
#打印最后一次结果
print((cv_results["test-rmse-mean"]).tail(1))
# 打印树的分裂情况
xg_reg = xgb.train(params=params, dtrain=data_matrix, num_boost_round=10)
xgb.plot_tree(xg_reg,num_trees=0)
plt.rcParams['figure.figsize'] = [80, 60]
plt.show()