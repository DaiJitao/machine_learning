#!/usr/bin/python
# -*- coding:utf-8 -*-

import csv
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
# from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LinearRegression, RidgeCV, LassoCV, ElasticNetCV
from pprint import pprint


def load_data(path):
    # pandas读入
    data = pd.read_csv(path)  # TV、Radio、Newspaper、Sales
    x = data[['TV', 'Radio', 'Newspaper']]
    # x = data[['TV', 'Radio']]
    y = data['Sales']
    print(x)
    print(y)
    return x, y, data


def show_true_data(x, y, data):
    # 绘制1
    plt.figure(facecolor='w')
    plt.plot(data['TV'], y, 'ro', label='TV')
    plt.plot(data['Radio'], y, 'g^', label='Radio')
    plt.plot(data['Newspaper'], y, 'mv', label='Newspaer')
    plt.legend(loc='lower right')
    plt.xlabel('广告花费', fontsize=16)
    plt.ylabel('销售额', fontsize=16)
    plt.title('广告花费与销售额对比数据', fontsize=18)
    plt.grid(b=True, ls=':')
    plt.show()


def show_true_data_3_plots(x, y, data):
    # 绘制2
    plt.figure(facecolor='w', figsize=(9, 10))
    plt.subplot(311)
    plt.plot(data['TV'], y, 'ro')
    plt.title('TV')
    plt.grid(b=True, ls=':')
    plt.subplot(312)
    plt.plot(data['Radio'], y, 'g^')
    plt.title('Radio')
    plt.grid(b=True, ls=':')
    plt.subplot(313)
    plt.plot(data['Newspaper'], y, 'b*')
    plt.title('Newspaper')
    plt.grid(b=True, ls=":")
    plt.tight_layout()
    plt.show()


def show_results(x_test, y_test, y_predicts, labels):
    plt.figure(facecolor='w')
    # plt.subplot(411)
    t = np.arange(len(x_test))
    plt.plot(t, y_test * 100, 'r-', linewidth=2, label='真实数据')
    plt.legend(loc='upper left')
    plt.title('线性回归预测销量', fontsize=18)
    plt.grid(b=True, ls=':')
    # ----------------------------------------------------------------------------
    count = 0
    colors = ["g-", "y-", "k--", "bo-"]
    index = 1
    for y_hat, label in zip(y_predicts, labels):
        index += 1
        # plt.subplot(4, 1, index)
        plt.plot(t, y_hat * 100, colors[count], linewidth=2, label=label)
        count += 1
        plt.legend(loc='upper left')
        # plt.title('线性回归预测销量', fontsize=18)
        plt.grid(b=True, ls=':')

    plt.show()


if __name__ == "__main__":
    path = '.\\Advertising.csv'
    x, y, data = load_data(path)

    mpl.rcParams['font.sans-serif'] = ['simHei']
    mpl.rcParams['axes.unicode_minus'] = False

    # show_true_data(x, y, data)
    # show_true_data_3_plots(x, y, data)

    x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.8, random_state=1)
    print(type(x_test))
    print(x_train.shape, y_train.shape)
    linreg = LinearRegression(fit_intercept=False,normalize=True)  # params: normalize=True,fit_intercept=False;
    model = linreg.fit(x_train, y_train)
    print(model)
    print("coef_=", linreg.coef_, " intercept_=", linreg.intercept_)
    print("RidgeCV===============================>>>")
    RidgeCV_model = RidgeCV(alphas=[0.01, 0.1, 1.0, 10.0], fit_intercept=False,normalize=True)  # 通过RidgeCV可以设置多个参数值，算法使用交叉验证获取最佳参数值
    RidgeCV_model.fit(x_train, y_train)  # 线性回归建模
    print("RidgeCV_model: ", RidgeCV_model)
    print("RidgeCV_model.coef_=", RidgeCV_model.coef_, " RidgeCV_model.intercept_=", RidgeCV_model.intercept_)
    print("LassoCV===================================================>>")
    lassoCV_res = LassoCV(alphas=[0.01, 0.1, 1.0, 10.0], fit_intercept=False,normalize=True)
    lassoCV_res.fit(x_train, y_train)  # 线性回归建模
    print("lassoCV_res: ", lassoCV_res)
    print("lassoCV_res.coef_=", lassoCV_res.coef_, " lassoCV_res.intercept_=", lassoCV_res.intercept_)

    order = y_test.argsort(axis=0)
    y_test = y_test.values[order]  # 真实数据
    x_test = x_test.values[order, :]
    # 预测数据
    y_hat = linreg.predict(x_test)
    ridgeCV_predict = RidgeCV_model.predict(x_test)
    print("ridgeCV_predict:\n", ridgeCV_predict)
    print("y_hat ", y_hat)
    lassoCV_predict = lassoCV_res.predict(x_test)

    mse = np.average((y_hat - np.array(y_test)) ** 2)  # Mean Squared Error
    rmse = np.sqrt(mse)  # Root Mean Squared Error
    print('MSE = ', mse, end=' ')
    print('RMSE = ', rmse)
    print('R2 = ', linreg.score(x_train, y_train))
    print('R2 = ', linreg.score(x_test, y_test))

    y_predicts = [y_hat, ridgeCV_predict, lassoCV_predict]
    labels = ["多元线性回归预测", "RidgeCV 预测", "lassoCV_predict 预测"]
    show_results(x_test, y_test, y_predicts, labels)
