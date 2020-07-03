'''
https://blog.csdn.net/jerr__y/article/details/61195257
'''
MNIST_data = r"E:\data\MNIST_data_sets\MNIST_data"

import tensorflow as tf
import numpy as np
from tensorflow.contrib import rnn

from tensorflow.examples.tutorials.mnist import input_data

# config = tf.ConfigProto()
# config.gpu_options.allow_growth = True


mnist = input_data.read_data_sets(MNIST_data, one_hot=True)
print(mnist.train.images.shape)

lr = 0.01  # 学习率
batch_size = 28 # tf.placeholder(tf.int32)

# 每个时刻的输入特征是28维的，就是每个时刻输入一行，一行有 28 个像素
input_size = 28
# 时序持续长度为28，即每做一次预测，需要先输入28行；# 一共28行
timestep_size = 28
# 每个隐含层的节点数,lstm单元的个数
hidden_size = 28
# LSTM layer 的层数
layer_num = 2
# 最后输出分类类别数量，如果是回归预测的话应该是 1
class_num = 10

_x = tf.placeholder(tf.float32, [None, 784])
X = tf.reshape(_x, [-1, 28, 28])
y = tf.placeholder(tf.float32, [None, class_num])
# keep_prob = tf.placeholder(tf.float32)
keep_prob = tf.placeholder(tf.float32, [])

# 2. 开始搭建 LSTM 模型，其实普通 RNNs 模型也一样

############################## start:定义好一层LSTM      #######################################
""" num_units 该层数的cell 个数"""
lstm_cell = rnn.BasicLSTMCell(num_units=hidden_size, forget_bias=1.0, state_is_tuple=True)
# 添加 dropout layer, 一般只设置 output_keep_prob
lstm_cell = rnn.DropoutWrapper(cell=lstm_cell, input_keep_prob=1.0, output_keep_prob=keep_prob)
############################## end:定义好一层LSTM      #######################################

# **步骤4：调用 MultiRNNCell 来实现多层 LSTM
multi_lstmCell = rnn.MultiRNNCell([lstm_cell] * layer_num, state_is_tuple=True)

init_state = multi_lstmCell.zero_state(batch_size, dtype=tf.float32)  # 初始化

outputs = list()
state = init_state
with tf.variable_scope('RNN-dai'):
    for timestep in range(timestep_size):  # 一共28行
        if timestep > 0:
            tf.get_variable_scope().reuse_variables()
        print("循环输入次数{}，数据\n{}".format(timestep, X[:, -1, :]))
        print(X.shape)
        print(X)
        (cell_output, state) = multi_lstmCell(X[:, timestep, :], state)
        print("(cell_output, state)=({}, {})".format(cell_output, state))
        outputs.append(cell_output)  #
h_state = outputs[-1]
W = tf.Variable(tf.truncated_normal([batch_size, class_num], stddev=0.1), tf.float32)
bias = tf.Variable(tf.constant(0.1, shape=[class_num]), dtype=tf.float32)

h_state = tf.transpose(h_state)
# print("W维度{}，h_sate维度:{}".format(W.shape, h_state.shape))
y_pred = tf.nn.softmax(tf.matmul(h_state, W) + bias)
# tf.nn.softmax_cross_entropy_with_logits(y_pred=y_pred,y=y)
# 损失和评估函数
print("真实值y:{}, 预测值y_pred:{}".format(y.shape, y_pred.shape))
cross_entropy = tf.nn.softmax_cross_entropy_with_logits(labels=y_pred, logits=tf.matmul(h_state, W) + bias)
# cross_entropy = -tf.reduce_mean(y * tf.log(y_pred))
train_op = tf.train.AdamOptimizer(lr).minimize(cross_entropy)

correct_prediction = tf.equal(tf.argmax(y_pred, 1), tf.argmax(y, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
print("==============>")

def main():
    sess = tf.Session()
    sess.run(tf.global_variables_initializer())
    for i in range(5000):

        batch = mnist.train.next_batch(batch_size)
        if (i + 1) % 100 == 0:
            train_accuracy = sess.run(accuracy,
                                      feed_dict={_x: batch[0], y: batch[1], keep_prob: 1.0})
            # 已经迭代完成的 epoch 数: mnist.train.epochs_completed
            print("Iter%d, step %d, training accuracy %g" % (mnist.train.epochs_completed, (i + 1), train_accuracy))

        # print("输入形状x:{}".format(batch[0].shape))
        # print("输入形状y:{}".format(batch[1].shape))
        sess.run(train_op, feed_dict={_x: batch[0], y: batch[1], keep_prob: 0.5,})

    # 计算测试数据的准确率
    # print(
    #     "test accuracy %g" % sess.run(accuracy, feed_dict={_x: mnist.test.images, y: mnist.test.labels, keep_prob: 1.0,
    #                                                        batch_size: mnist.test.images.shape[0]}))
if __name__ == '__main__':
    main()

