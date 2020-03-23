import torch
import numpy as np
import numpy
from torch.autograd import Variable
import matplotlib.pyplot as plt


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
    print(w.grad)
    print(b.grad)

def demo3():
    """
    比如有一个函数，y=x的平方（y=x2）,在x=3的时候它的导数为6，我们通过代码来演示这样一个过程。
    :return:
    """
    x = Variable(torch.Tensor([3]), True)

    y = torch.pow(x,2)
    y.backward() # 求导

    print(x.grad) # 在x=3的时候它的导数为6

def demo4(x):
    w = numpy.array([11,8,9]).reshape(1,3)
    b = 4
    x = np.array(x).reshape(3,1)
    y = np.dot(w,x) + b

    return y[0][0]


if __name__ == '__main__':
    x1 = range(1, 10)
    x2 = range(10,20)
    x3 = range(12, 22)
    y = []
    for i in zip(x1, x2, x3):
        y.append(demo4(i))
    plt.plot(x1, y)
    plt.show()