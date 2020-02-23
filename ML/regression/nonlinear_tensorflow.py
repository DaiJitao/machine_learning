import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import time

mpl.rcParams['font.sans-serif'] = ['simHei']
mpl.rcParams['axes.unicode_minus'] = False


def load_data():
    x = np.linspace(-.5, .5, 500)[:, np.newaxis]

    noise = np.random.normal(0, 0.1, x.shape)
    y = x + noise
    return x.astype(np.float32), y.astype(np.float32)


class NolinearRegression():
    def __init__(self, x_data, y_data):
        self.x_data = x_data
        self.y_data = y_data

    def train_model(self, lr=0.1, times=1000):
        self.x = tf.placeholder(dtype=tf.float32, shape=[None, 1])
        self.y = tf.placeholder(dtype=tf.float32, shape=[None, 1])
        # first layer
        weight_1 = tf.Variable(tf.random_normal(dtype=tf.float32, shape=[1, 10]))
        b_1 = tf.Variable(tf.random_normal(dtype=tf.float32, shape=[10]))
        wx_b_1 = tf.add(tf.matmul(x, weight_1), b_1)
        layer_1 = tf.nn.tanh(wx_b_1)
        #  out layer
        out_weights = tf.Variable(tf.random_normal(dtype=tf.float32, shape=[10, 1]))
        out_b = tf.Variable(tf.random_normal(dtype=tf.float32, shape=[1]))
        wx_out = tf.add(tf.matmul(layer_1, out_weights), out_b)
        layer_out = tf.nn.tanh(wx_out)

        # 二次代价函数
        loss = tf.reduce_mean(tf.square(layer_out - y))

        # 使用梯度下降法训练
        train_step = tf.train.GradientDescentOptimizer(lr).minimize(loss)

        init = tf.global_variables_initializer()
        with tf.Session() as sess:
            sess.run(init)
            for _ in range(times):
                sess.run(train_step, feed_dict={self.x: self.x_data, self.y: self.y_data})
            # 获得预测值
            prediction_value = sess.run(layer_out, feed_dict={self.x: self.x_data})
        return prediction_value


if __name__ == '__main__':
    x, y = load_data()
    times = 4000
    regress = NolinearRegression(x, y)
    prediction_value1 = regress.train_model(times)
    prediction_value2 = regress.train_model(0.01, times)
    time.sleep(1)
    plt.figure()
    plt.plot(x, y, label="真实数据")
    plt.plot(x, prediction_value1, label="lr=0.1 times="+ str(times)+" 预测数据")
    plt.plot(x, prediction_value2, "r--", label="lr=.01,times="+ str(times)+" 预测数据")
    plt.grid(b=True, ls=':')
    plt.legend()
    plt.show()
