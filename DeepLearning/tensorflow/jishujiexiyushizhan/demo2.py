from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from keras.preprocessing.sequence import pad_sequences
from numpy import array

data = ['cold', 'cold', 'warm', 'cold', 'hot', 'hot', 'warm', 'cold', 'warm', 'hot']
values = array(data)
print(values)
# 整数编码
label_encoder = LabelEncoder()
print(label_encoder.fit_transform(values))
# print(label_encoder.inverse_transform([1]))
integer_encoded = label_encoder.fit_transform(values)
# 独热编码
one_hot = OneHotEncoder(sparse=False)
integer_encoded = integer_encoded.reshape((len(integer_encoded), 1))
one_hot_encoded = one_hot.fit_transform(integer_encoded)
print(one_hot_encoded)
print(one_hot_encoded.shape)

import tensorflow as tf
import matplotlib.pyplot as plt

'''以下为CNN实现'''
from tensorflow.examples.tutorials.mnist import input_data
# 数据路径
data_path = r"F:\pycharm_workspce\dai_github\myproject\machine_learning\DeepLearning\tensorflow\MNIST_data"
mnist = input_data.read_data_sets(train_dir=data_path, one_hot=True)

print(mnist.train)
