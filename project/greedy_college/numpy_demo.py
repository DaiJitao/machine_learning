# 线性代数常用函数
# dot 矩阵乘法
# trace 计算对角元素的和
# det 计算矩阵的行列式
# eig 计算特征值和特征向量
# inv 计算矩阵的逆


import matplotlib.pyplot as plt
import numpy as np

x = [[1, 2, 3], [4, 5, 6]]
y = [[1, 2], [4, 5], [7, 8]]
np.dot(x, y)

if __name__ == '__main__':
    f = plt.figure()
    fgs = 2
    for i in range(fgs):
        f.add_subplot(fgs, 1, i + 1)
        position = 0
        walk = [position]
        steps = 600
        for i in range(steps):
            step = 1 if np.random.randint(0, 2) else -1
            position += step
            walk.append(position)

        mean = np.mean(walk)
        print("mean: ", mean)
        plt.plot(walk)
        plt.plot([mean] * len(walk), "r--")
        walk = np.abs(walk)
        print(walk[walk > 10].argmax())
    plt.show()
