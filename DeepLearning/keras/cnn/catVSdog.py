'''
猫狗数据集
'''

import keras.losses as losses
from keras.layers import Dense, Flatten, MaxPool2D, Conv2D
from keras import metrics
from keras import models
from keras import optimizers
from keras import activations


def build_model(image_x, image_y, channels):
    model = models.Sequential()
    model.add(Conv2D(32, (3, 3), input_shape=(image_x, image_y, channels), activation=activations.relu))
    model.add(MaxPool2D((2, 2)))
    model.add(Conv2D(64, (3, 3), activation=activations.relu))
    model.add(MaxPool2D((2, 2)))
    model.add(128, (3, 3))
    model.add(MaxPool2D((2, 2)))
    model.add(128, (3, 3))
    model.add(MaxPool2D((2, 2)))
    model.add(Flatten())
    model.add(Dense(512, activation=activations.relu))
    model.add(Dense(1, activation=activations.sigmoid))
    model.compile(optimizer=optimizers.RMSprop, loss=losses.binary_crossentropy, metrics=[metrics.binary_accuracy])
    def train(model):
        model.fit()
