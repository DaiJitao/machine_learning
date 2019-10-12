import tensorflow as tf

v1 = tf.constant([[1, 2, 3], [4, 5, 6]], dtype=tf.int16)

sess = tf.InteractiveSession()

s = tf.reduce_mean(v1, axis=0).eval()
print(s)

sess.close()