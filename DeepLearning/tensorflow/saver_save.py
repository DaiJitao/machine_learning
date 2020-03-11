import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import numpy as np
import os

mnist = input_data.read_data_sets("./MNIST_data", one_hot=True)

batch_size = 100
n_batch = mnist.train.num_examples // batch_size

times =111

x = tf.placeholder(dtype=tf.float32, shape=[None, 784])
y = tf.placeholder(dtype=tf.float32, shape=[None, 10])

w = tf.Variable(tf.random_uniform(shape=[784, 10], dtype=tf.float32))
b = tf.Variable(tf.random_uniform(shape=[10], dtype=tf.float32))
wx_b = tf.add(tf.matmul(x, w), b)
prediction = tf.nn.softmax(wx_b)

loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y, logits=prediction))

train_step = tf.train.GradientDescentOptimizer(0.2).minimize(loss)

init = tf.global_variables_initializer()

correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(prediction,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

saver = tf.train.Saver()


def train():
    with tf.Session() as sess:
        sess.run(init)
        for epoch in range(times):
            for batch in range(n_batch):
                batch_xs, batch_ys = mnist.train.next_batch(batch_size)
                sess.run(train_step, feed_dict={x: batch_xs, y: batch_ys})

            acc = sess.run(accuracy, feed_dict={x: mnist.test.images, y: mnist.test.labels})
            print("Iter " + str(epoch) + ",Testing Accuracy " + str(acc))
        if not os.path.exists("E:/data/models/saver_save"):
            os.makedirs("E:/data/models/saver_save")

        saver.save(sess, "E:/data/models/saver_save/test_model.ckpt")

def restore(model):
    with tf.Session() as sess:
        sess.run(init)
        print(sess.run(accuracy, feed_dict={x: mnist.test.images, y: mnist.test.labels}))
        saver.restore(sess, model)
        print(sess.run(accuracy, feed_dict={x: mnist.test.images, y: mnist.test.labels}))



if __name__ == '__main__':
    restore(model="E:/data/models/saver_save/test_model.ckpt")



