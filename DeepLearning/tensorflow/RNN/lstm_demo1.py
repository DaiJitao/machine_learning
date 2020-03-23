from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf
from  tensorflow import nn
from tensorflow.contrib import rnn

MNIST_data_file = r"E:\data\MNIST_data_sets\MNIST_data"
data = input_data.read_data_sets(MNIST_data_file, one_hot=True)

n_input = 28
n_steps = 28
# The number of features in the hidden layer
n_hidden = 128
n_classes = 10

learning_rate = .001
training_iters = 100000
batch_size = 128
display_step = 10

x = tf.placeholder([None, n_steps, n_input], dtype=tf.float32)
y = tf.placeholder([None, 10], dtype=tf.float32)

weights = {
    'out': tf.Variable(tf.random_normal([n_hidden, n_classes]))
}

bias = {
    "out": tf.Variable(tf.random_normal([n_classes]))
}


def RNN(x, weights, biases):
    print("input: x = {}".format(x))
    x = tf.transpose(x, [1, 0, 2])
    print("x transpose: {}".format(x))
    x = tf.reshape(x, [-1, n_input])
    print("x reshape:{}".format(x))
    x = tf.split(axis=0, num_or_size_splits=n_steps, value=x)
    x = tf.split(axis=0, num_or_size_splits=n_steps, value=x)
    lstm_cell = nn.rnn_cell.BasicLSTMCell(n_hidden, forget_bias=1.0)
    outputs, states = rnn.rnn(lstm_cell, x, dtype=tf.float32)
    return tf.matmul(outputs[-1], weights['out']) + biases['out']
