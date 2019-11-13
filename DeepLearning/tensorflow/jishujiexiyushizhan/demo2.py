from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from keras.preprocessing.sequence import pad_sequences
from numpy import array

data = ['cold', 'cold', 'warm', 'cold', 'hot', 'hot', 'warm', 'cold', 'warm', 'hot']
values = array(data)
print(values)
# 整数编码
label_encoder = LabelEncoder()
# print(label_encoder.fit_transform(values))
# print(label_encoder.inverse_transform([1]))
integer_encoded = label_encoder.fit_transform(values)
# 独热编码
one_hot = OneHotEncoder(sparse=False)
integer_encoded = integer_encoded.reshape((len(integer_encoded), 1))
one_hot_encoded = one_hot.fit_transform(integer_encoded)

import tensorflow as tf
import matplotlib.pyplot as plt

'''以下为CNN实现'''
from tensorflow.examples.tutorials.mnist import input_data

# 数据路径
data_path = r"F:\pycharm_workspce\dai_github\myproject\machine_learning\DeepLearning\tensorflow\MNIST_data"
mnist = input_data.read_data_sets(train_dir=data_path, one_hot=True)

# 网络超参数
lr = 0.001
trainig_times = 200000
batch_size = 128
display_step = 10
# 定义网络参数
n_input = 784
n_classes = 10
dropout = 0.75
# 占位符
x = tf.placeholder(tf.float32, [None, n_input])
y = tf.placeholder(tf.float32, [None, n_classes])
keep_p = tf.placeholder(tf.float32)

batch_x, batch_y = mnist.train.next_batch(batch_size)
print(batch_x)


# 构建网络模型
def build_model():
    pass


def conv2d(name, x, W, b, strides=1):
    x = tf.nn.conv2d(x, W, strides=[1, strides, strides, 1], padding='SAME')
    x = tf.nn.bias_add(x, b)
    return tf.nn.relu(x, name=name)


def pooling(name, x, size=2):
    return tf.nn.max_pool(x, ksize=[1, size, size, 1], strides=[1, size, size, 1], padding='SAME', name=name)


def norm(name, l_input, lsize=4):
    return tf.nn.lrn(l_input, lsize, bias=1.0, alpha=0.001 / 9.0, beta=0.75, name=name)


import numpy as np

vs = np.arange(1., 11, 2.)
p = tf.placeholder(tf.float32)
c = tf.constant(3.)
product = tf.multiply(p, c)
with tf.Session() as sess:
    for i in vs:
        print(sess.run(product, feed_dict={p: i}))

my_array = np.array([[1.0, 3., 5., 7., 9.],
                     [-2., 0., 2., 4., 6.],
                     [-6., -3., 0., 3., 6.]])
x_vals = np.array([my_array, my_array+1])
print(x_vals)
