# MINIST数据集
import tensorflow as tf
import os

X = tf.placeholder(dtype=tf.float32, shape=(None, 784))
Y = tf.placeholder(dtype=tf.float32, shape=(None, 10))


# 初始化参数
def init_weights(shape):
    return tf.Variable(tf.random.truncated_normal(shape=shape, stddev=0.01), dtype=tf.float32)


w_h1 = init_weights([784, 625])
w_h2 = init_weights((625, 625))
w_o = init_weights((625, 10))


# 定义模型
def model(X, w_h1, w_h2, w_o, input_keep_prob, hidden_keep_prob):
    # 第一个全连接层
    x = tf.nn.dropout(X, keep_prob=input_keep_prob)
    h1 = tf.nn.relu(tf.matmul(x, w_h1))

    # 第二个全连接层
    h1 = tf.nn.dropout(h1, keep_prob=hidden_keep_prob)
    h2 = tf.nn.relu(tf.matmul(h1, w_h2))

    # 输出层
    out = tf.nn.dropout(h2, hidden_keep_prob)
    out = tf.matmul(out, w_o)
    return out

# 调用模型
input_keep_prob = tf.placeholder(tf.float32)
hidden_keep_prob = tf.placeholder(tf.float32)
py_x = model(X, w_h1, w_h2, w_o=w_o, input_keep_prob=input_keep_prob, hidden_keep_prob=hidden_keep_prob)

# 定义损失函数
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=py_x, labels=Y))
train_op = tf.train.RMSPropOptimizer(learning_rate=0.01, decay=0.9).minimize(cost)
# 预测
predict_op = tf.argmax(py_x, 1)

# 定义存储路径
path = "./model"
if not os.path.exists(path):
    os.mkdir(path)


global_step = tf.Variable(0, name="global_step1", trainable=False)

saver = tf.train.Saver()


with tf.Session() as sess:
    tf.initialize_all_variables().run()
    start = global_step.eval()
    print("开始：", start)