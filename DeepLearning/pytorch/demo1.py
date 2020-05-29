import torch
import numpy as np
import numpy
from torch.autograd import Variable
import matplotlib.pyplot as plt
from torch.distributions.bernoulli import Bernoulli


def demo1():
    a = numpy.arange(2, 8).reshape([3, 2])
    print(a)
    a = torch.Tensor(a)
    print(a)
    print(a.size())
    print(type(a))
    print(type(a.numpy()))
    print(torch.cuda.is_available())
    print(torch.Tensor([1]))


def demo2():
    x = Variable(torch.Tensor([1]), True)
    w = Variable(torch.Tensor([2]), True)
    b = Variable(torch.Tensor([3]), True)

    y = w * x + b
    print(y)
    # 计算梯度
    y.backward()

    print("x=1的导数", x.grad)
    print("w导数：", w.grad)
    print("b导数：", b.grad)


def demo5():
    pass

if __name__ == '__main__':
    a = torch.randn((3,2))

    print(a)


def demo3():
    """
    比如有一个函数，y=x的平方（y=x2）,在x=3的时候它的导数为6，我们通过代码来演示这样一个过程。
    :return:
    """
    x = Variable(torch.Tensor([3]), True)

    y = torch.pow(x, 2)
    y.backward()  # 求导

    print(x.grad)  # 在x=3的时候它的导数为6


def demo4(x):
    w = numpy.array([11, 8, 9]).reshape(1, 3)
    b = 4
    x = np.array(x).reshape(3, 1)
    y = np.dot(w, x) + b

    return y[0][0]


def forward(x):
    return x * w


def loss(x, y):
    y_pred = forward(x)
    return (y_pred - y) ** 2


torch.manual_seed(1234)
a = torch.randn(4, 4)
print(a)
print(torch.sigmoid(a))
print(torch.Tensor(4, 4).uniform_(0, 1))
print()
if __name__ == '__main__1':
    w = Variable(torch.Tensor([1.0]), True)
    x_data = [11, 22, 33.0]
    y_data = [21., 14., 64]
    for epoch in range(11):
        for x_val, y_val in zip(x_data, y_data):
            l = loss(x_val, y_val)
            l.backward()
            print("\t初始化w: x={}, y={}, w={}, w.grad={} ".format(x_val, y_val, w.data[0], w.grad.data[0]))
            w.data = w.data - 0.01 * w.grad.data[0]
            print("\t更新完w: x={}, y={}, w={}, w.grad={} ".format(x_val, y_val, w.data[0], w.grad.data[0]))
            #
            w.grad.data.zero_()
            print("\t导数置零：x={}, y={}, w={}, w.grad={} ".format(x_val, y_val, w.data[0], w.grad.data[0]))
            print("\n")
        print("epoch:{}, loss={} \n".format(epoch, l.data[0]))

    dist = Bernoulli(torch.Tensor([.3,.6,.9]))
    print(dist.sample())