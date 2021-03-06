import torch
import torch.nn as nn
import torch.optim as optim
from torch.autograd import Variable
import numpy as np
import matplotlib.pyplot as plt
import sys

"""
# 一元线性回归
"""

np.random.seed(111)

def load_data(x, a=2.0123, b=6.456):
    y = []
    for i in x:
        t = a * i + b + np.random.randint(low=0, high=3)
        y.append(t)
    return y


# 生成数据
size = 50
x_train = range(0, size)
y_train = load_data(x_train)


# tensor
x_train = torch.Tensor(x_train).reshape(size,1)
y_train = torch.Tensor(y_train).reshape(size,1)


class LR(nn.Module):
    def __init__(self):
        super(LR, self).__init__()
        # 第一个1 为输入维度1， 第二个为输出维度
        self.linear = nn.Linear(1, 1)

    def forward(self,x):
        out = self.linear(x)
        return out


if __name__ == '__main__':
    model = LR()

    # 定义损失函数
    criterion = nn.MSELoss()

    # 定义优化器
    optimizer = optim.Rprop(model.parameters(), lr=.0001)

    # 训练模型
    num_epoches = 1000
    for epach in range(num_epoches):
        inputs = Variable(x_train)
        target = Variable(y_train)  # 实际值
        out = model(inputs)  # 预测值
        loss = criterion(out, target)
        # 优化器用于更新网络参数
        optimizer.zero_grad()
        # 求导
        loss.backward()
        # 更新参数
        optimizer.step()
        if (epach + 1) % 1 == 0:
            print("epoch:{}, loss:{:.2f}".format(epach, loss.data))

    model.eval()
    predit = model(Variable(x_train))
    predit = predit.data.numpy()

    plt.figure()
    plt.subplot(1, 1, 1)
    plt.plot(x_train, y_train, label="train data")
    plt.plot(x_train,predit,label='predict data')
    plt.legend()
    plt.show()
    print("退出。。。")
    sys.exit(1)




