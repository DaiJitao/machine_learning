"""
get data:
#get the mnist data
# wget http://deeplearning.net/data/mnist/mnist.pkl.gz
"""

from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf

import logging
import matplotlib.pyplot as plt
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

mnist = input_data.read_data_sets(train_dir="./data/mnist/", one_hot=True)

# Parameters
learning_rate = 0.001
training_epochs = 30
batch_size = 100
display_step = 1

# Network Parameters
n_hidden_1 = 256  # 1st layer number of features
n_hidden_2 = 512  # 2nd layer number of features
n_input = 784  # MNIST data input (img shape: 28*28)
n_classes = 10  # MNIST total classes (0-9 digits)

weights = {
    'h1': tf.Variable(tf.random_normal([n_input, n_hidden_1], stddev=1.0, dtype=tf.float32)),
    'h2': tf.Variable(tf.random_normal([n_hidden_1, n_hidden_2], stddev=1.0, dtype=tf.float32)),
    'out': tf.Variable(tf.random_normal([n_hidden_2, n_classes], stddev=1.0, dtype=tf.float32))
}
biases = {
    'b1': tf.Variable(tf.random_normal([n_hidden_1], stddev=1.0, dtype=tf.float32)),
    'b2': tf.Variable(tf.random_normal([n_hidden_2], stddev=1.0, dtype=tf.float32)),
    'out': tf.Variable(tf.random_normal([n_classes], stddev=1.0, dtype=tf.float32))
}


def multilayer_perceptron(x, weights, biases):
    layer_1 = tf.add(tf.matmul(x, weights['h1']), biases['b1'])
    layer_1 = tf.nn.relu(layer_1)

    layer_2 = tf.add(tf.matmul(layer_1, weights['h2']), biases['b2'])
    layer_2 = tf.nn.relu(layer_2)

    out_layer = tf.matmul(layer_2, weights['out']) + biases['out']
    return out_layer



def main(training_epochs):
    x = tf.placeholder(tf.float32, [None, n_input])
    y = tf.placeholder(tf.float32, [None, n_classes])
    # Construct model
    pred = multilayer_perceptron(x, weights, biases)

    # Define loss and optimizer
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=pred, labels=y))
    optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)

    # initializing the variables
    init = tf.global_variables_initializer()

    # launch the graph
    with tf.Session() as sess:
        print("start initing")
        sess.run(init)
        print("init successfully!")
        epoches = []
        for epoch in range(training_epochs):
            avg_cost = 0
            total_batch = int(mnist.train.num_examples / batch_size)
            for i in range(total_batch):
                batch_x, batch_y = mnist.train.next_batch(batch_size)
                _, c = sess.run([optimizer, cost], feed_dict={x: batch_x, y: batch_y})
                avg_cost += c / total_batch
            epoches.append(avg_cost)
            if epoch % display_step == 0:
                print("Epoch:", '%04d' % (epoch + 1), "cost=", "{:.9f}".format(avg_cost))
        print("Optimization Finished!")

        # Test model
        correct_prediction = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))
        # Calculate accuracy
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
        print("Accuracy:", accuracy.eval({x: mnist.test.images, y: mnist.test.labels}))
        return epoches


def plot_cost(training_epochs, cost_values):
    import matplotlib.pyplot as plt
    plt.figure()
    line = plt.plot(range(training_epochs), cost_values)
    line.set(color='g', linewidth=2.0)
    plt.show()


if __name__ == '__main__':
    plt.figure()
    training_epochs = 30
    cost_values_1 = main(training_epochs)

    #
    training_epochs = 60
    cost_values_2 = main(training_epochs)
    line = plt.plot(range(training_epochs), cost_values_2)
    plt.show()

