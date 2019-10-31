
from keras import models
from keras import layers
import tensorflow as tf

def demo():
    model = models.Sequential()
    model.add(layers.Dense(32, activation="relu", input_shape=(784,)))
    model.add(layers.Dense(10, activation="softmax"))

    print('ok')


#加载数据
from keras.datasets import imdb

(train_data, train_labels), (test_data, test_labels) = imdb.load_data(num_words=10000)
print(type(train_data))
print(train_data.shape)
