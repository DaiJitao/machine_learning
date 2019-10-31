import numpy as np
import matplotlib.pyplot as plt
np.set_printoptions(suppress=True) # 舍弃科学计数法

def sotfmax(x):
    temp = [np.exp(i) for i in x]
    sum_ = np.sum(temp)
    return np.array([i / sum_ for i in temp])


if __name__ == "__main__":
    x = np.linspace(0, 100, 1000)
    print(type(x))
    print(x.shape)
    y = sotfmax(x)

    plt.plot(x, y)
    print(np.round(y, decimals=10))
    print(np.sum(y))
    plt.show()
