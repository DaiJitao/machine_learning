import tensorflow as tf

tf.set_random_seed(1)

with tf.name_scope("a_name_scope"):
    initializer = tf.constant_initializer(value=1)
    # 两种创建variable的途径
    # tf.get_variable要定义一个initializer
    # name_scope 对tf.get_variable无效
    var1 = tf.get_variable(name='var1', shape=[1], dtype=tf.float32, initializer=initializer)

    var2 = tf.Variable(name='var2', initial_value=[2], dtype=tf.float32)
    var21 = tf.Variable(name='var2', initial_value=[2.1], dtype=tf.float32)
    var22 = tf.Variable(name='var2', initial_value=[2.2], dtype=tf.float32)

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    # 分别打印varibale的名字和值
    print(var1.name)
    print(sess.run(var1))
    print(var2.name)
    print(sess.run(var2))
    print(var21.name)
    print(sess.run(var21))
    print(var22.name)
    print(sess.run(var22))


with tf.variable_scope("a_variable_scope") as scope:
    initializer=tf.constant_initializer(value=3)
    var3=tf.get_variable(name="var4",shape=[1],dtype=tf.float32,initializer=initializer)
    var4=tf.Variable(name='var3',initial_value=[4],dtype=tf.float32)
    #可以重复调用之前创造的变量，但是tf.Variable是不可行的，只能重新创建一个
    #a_variable_scope/var4:0
    # [ 4.]
    # a_variable_scope/var4_1:0
    # [ 4.]
    #var4_reuse=tf.Variable(name='var4',initial_value=[4],dtype=tf.float32)

    #使用tf.get_variable重复调用var3,要先强调后面的要重复利用
    #scope.reuse_variables()会先再前面搜索是否已经存在，重复利用得到的两个变量是同一个变量
    scope.reuse_variables()
    var3_reuse=tf.get_variable(name='var4')
print("++++++++++++")
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    #分别打印varibale的名字和值
    print(var3.name)
    print(sess.run(var3))
    print(var4.name)
    print(sess.run(var4))
    print(var3_reuse.name)
    print(sess.run(var3_reuse))


from tensorflow.models.tutorials.rnn.ptb import reader
