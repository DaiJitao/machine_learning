# coding: utf-8

import os
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
from DeepLearning.utils import mkdir

log_file = r"E:\log\tensorflow_tensorboard"
mkdir(log_file)
MNIST_data = r"E:\data\MNIST_data_sets\MNIST_data"
# 载入数据集
mnist = input_data.read_data_sets("MNIST_data", one_hot=True)

# 每个批次的大小
batch_size = 100
# 计算一共有多少个批次
n_batch = mnist.train.num_examples // batch_size

with tf.name_scope("input"):
    # 定义两个placeholder
    x = tf.placeholder(tf.float32, [None, 784], name="input_x")
    y = tf.placeholder(tf.float32, [None, 10], name="input_y")
with tf.name_scope("layer"):
    with tf.name_scope("weights"):
        with tf.name_scope("w"):
            # 创建一个简单的神经网络
            W = tf.Variable(tf.zeros([784, 10]), name="W")
        with tf.name_scope("biases"):
            b = tf.Variable(tf.zeros([10]))
        with tf.name_scope("wx_plus_b"):
            wx_plus_b = tf.matmul(x, W) + b
        with tf.name_scope("softmax_prediction"):
            prediction = tf.nn.softmax(wx_plus_b)

# 二次代价函数
with tf.name_scope("loss-function"):
    loss = tf.reduce_mean(tf.square(y - prediction),name="loss")

with tf.name_scope("train"):
    # 使用梯度下降法
    train_step = tf.train.GradientDescentOptimizer(0.2).minimize(loss)

# 初始化变量
init = tf.global_variables_initializer()

# 结果存放在一个布尔型列表中
correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(prediction, 1))  # argmax返回一维张量中最大的值所在的位置
# 求准确率
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

with tf.Session() as sess:
    sess.run(init)

    print("图已经保存--" + log_file)
    for epoch in range(200):
        for batch in range(n_batch):
            batch_xs, batch_ys = mnist.train.next_batch(batch_size)
            sess.run(train_step, feed_dict={x: batch_xs, y: batch_ys})

        acc = sess.run(accuracy, feed_dict={x: mnist.test.images, y: mnist.test.labels})
        print("Iter " + str(epoch) + ",Testing Accuracy " + str(acc))
    writer = tf.summary.FileWriter(log_file, sess.graph)
"""
tensorboard --logdir=E:\log\tensorflow_tensorboard
"""
