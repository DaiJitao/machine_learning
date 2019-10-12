import tensorflow.examples.tutorials.mnist.input_data as input_data
import tensorflow as tf

# initialize
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)
x = tf.placeholder(tf.float32, [None, 784])
y_ = tf.placeholder("float", [None, 10])

W1 = tf.Variable(tf.zeros([784, 256]))
b1 = tf.Variable(tf.zeros([256]))

W2 = tf.Variable(tf.zeros([256, 10]))
b2 = tf.Variable(tf.zeros([10]))


y1 = tf.nn.softmax(tf.add(tf.matmul(x, W1), b1))
y2 = tf.nn.softmax(tf.add(tf.matmul(y1, W2), b2))

# cross_entropy = -tf.reduce_sum(y_ * tf.log(y2))
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=y2, labels=y_))
train_step = tf.train.GradientDescentOptimizer(0.001).minimize(cost)
# train
init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)
for i in range(1000):
    print("训练批次 ", i)
    batch_xs, batch_ys = mnist.train.next_batch(128)
    sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})
# predict
correct_prediction = tf.equal(tf.argmax(y2, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
print(sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels}))
sess.close()
