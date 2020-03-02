import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
from DeepLearning.utils import mkdir

input_data_file = "./MNIST_data"

mnist = input_data.read_data_sets(input_data_file, one_hot=True)
"""
input: (None,28*28)
layer1:(28*28,512)
layee2:(512,256)
out:(256,10)
"""

display_step = 500

image_weight = 28
image_hight = 28

batch_size = 100
# 计算一共有多少个批次
n_batch = mnist.train.num_examples // batch_size

with tf.name_scope("input"):
    x = tf.placeholder(dtype=tf.float32, shape=[None, 28 * 28], name="input-x")
    Y = tf.placeholder(dtype=tf.float32, shape=[None,10], name="input-y")

with tf.name_scope("weights_biases"):
    with tf.name_scope("weights"):
        layer1_w = tf.Variable(tf.random_normal(shape=[image_hight * image_weight, 512]), dtype=tf.float32,
                               name="layer1_weights")
        layer2_w = tf.Variable(tf.random_normal(shape=[512, 256]), dtype=tf.float32,
                               name="layer2_weights")
        out_w = tf.Variable(tf.random_normal(shape=[784, 10]), dtype=tf.float32,
                            name="out_weights")

    with tf.name_scope("biases"):
        layer1_b = tf.Variable(tf.random_normal(shape=[512]), dtype=tf.float32,
                               name="layer1_biase")
        layer2_b = tf.Variable(tf.random_normal(shape=[256]), dtype=tf.float32,
                               name="layer2_biase")
        out_b = tf.Variable(tf.random_normal(shape=[10]), dtype=tf.float32,
                            name="out_biase")

with tf.name_scope("layer"):
    # wx_plus_b_1 = tf.add(tf.matmul(x, layer1_w), layer1_b)
    # layer1 = tf.nn.softmax(wx_plus_b_1)
    # wx_plus_b_2 = tf.add(tf.matmul(layer1, layer2_w), layer2_b)
    # layer2 = tf.nn.softmax(wx_plus_b_2)
    out_wx_plus_b = tf.add(tf.matmul(x, out_w), out_b)
    out = tf.nn.softmax(out_wx_plus_b)

with tf.name_scope("loss"):
    loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=out, labels=Y))

with tf.name_scope('optimization'):
    # opt = tf.train.GradientDescentOptimizer(learning_rate=.2).minimize(loss)
    opt = tf.train.AdamOptimizer(learning_rate=.4).minimize(loss)
    # opt = tf.train.RMSPropOptimizer(learning_rate=.2).minimize(loss)****


correct_prediction = tf.equal(tf.argmax(out,1), tf.argmax(Y,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

init = tf.global_variables_initializer()


logdir = "E:/data/tensorboard/log"
with tf.Session() as sess:
    sess.run(init)
    mkdir(logdir)
    writer = tf.summary.FileWriter(logdir,sess.graph)
    avg_cost = 0
    for Epoch in range(1000):
        for i in range(n_batch):
            batch_xs, batch_ys = mnist.train.next_batch(batch_size)
            opt_, c_ = sess.run([opt, loss], feed_dict={x: batch_xs, Y: batch_ys})

            # avg_cost += c_ / n_batch
            # if (i + 1) % display_step == 0:
            #     print("in-Epoch: {0}  cost={1}".format(Epoch + 1, avg_cost))
        # print("--------------------------->>>")
        acc = sess.run(accuracy, feed_dict={x: mnist.test.images, Y: mnist.test.labels})
        print("Epoch: {0}  Acc={1}%".format(Epoch + 1, acc*100))

    print("finished!")
