import tensorflow as tf



b_data = [1,2]
b = tf.placeholder(dtype=tf.float32, shape=[2,1])
A = tf.constant(value=[[11],
                       [12]],dtype=tf.float32)
c = tf.Variable(tf.zeros([10]))
print(c.shape, c.get_shape())


sess = tf.InteractiveSession()

sess.close()