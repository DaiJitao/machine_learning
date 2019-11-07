from keras.losses import binary_crossentropy
from keras import models
from keras import layers
from keras import activations
from keras.layers import Flatten, Dense
from keras.datasets import mnist
from keras.utils import to_categorical
from keras import optimizers
from keras import losses
from keras import metrics
import time
import pickle
import matplotlib.pyplot as plt
import h5py
import pandas as pd
import numpy as np


def load_data():
    (train_images, train_labels), (test_images, test_labels) = mnist.load_data()
    train_images = train_images.reshape((60000, 28, 28, 1))
    train_images = train_images.astype('float32') / 255
    test_images = test_images.reshape((10000, 28, 28, 1))
    test_images = test_images.astype('float32') / 255
    train_labels = to_categorical(train_labels)
    test_labels = to_categorical(test_labels)
    return (train_images, train_labels), (test_images, test_labels)


def load_haimo_data():
    """
    加载数据：训练集
    :return:
    """
    file = r"E:\比赛\新建文件夹\train\train_pre_data.h5"
    file_label = r"F:\pycharm_workspce\dai_github\machine_learning\data\train_pre_label.csv"
    labels = pd.read_csv(file_label)
    f = h5py.File(file, mode="r")
    data = f['data']
    print(data)
    res = []
    for i in range(len(data)):
        # 样例数
        exampls = data[i]
        # 灰度数
        grays = np.array(exampls[0])
        # 塑型
        temp = grays.reshape((79,95,79))
        res.append(temp)

    data_res = np.array(res)
    f.close()
    y = labels['label']
    y = to_categorical(y)
    return data_res, y


def build_model(input_shape=(79, 95, 79)):
    model = models.Sequential()

    model.add(layers.Conv2D(32, kernel_size=(3, 3), activation=activations.relu, input_shape=input_shape))
    model.add(layers.MaxPool2D(pool_size=(2, 2)))
    model.add(layers.Conv2D(512, kernel_size=(3, 3), activation=activations.relu))
    model.add(layers.MaxPool2D(pool_size=(2, 2)))
    model.add(layers.Conv2D(128, (3, 3), activation=activations.relu))
    model.add(layers.MaxPool2D(pool_size=(2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation=activations.relu))
    model.add(Flatten())
    model.add(Dense(128, activation=activations.relu))
    model.add(Dense(64, activation=activations.relu))
    model.add(Dense(3, activation=activations.softmax))
    model.summary()
    return model


def main(x,y,history_file):

    model = build_model()
    model.compile(optimizer=optimizers.RMSprop(lr=0.01), loss=losses.categorical_crossentropy,
                  metrics=[metrics.binary_accuracy])
    start = time.time()
    history = model.fit(x=x, y=y, epochs=10, batch_size=20, validation_split=.1)
    end = time.time()
    print("耗时（分钟）：", (end - start) / 60)
    # 历史数据保存
    pickle.dump(history, open(file=history_file, mode='wb'))
    # acc = model.evaluate(x=test_images, y=test_labels)
    # print(acc)


def plot(history_file):
    history = pickle.load(open(history_file, mode="rb"))
    h = history.history
    print(h)
    # 训练损失
    loss = h['loss']
    # 验证损失
    validation_loss = h['val_loss']
    # 训练批次
    epochs = range(1, len(loss) + 1)
    # 训练精度
    accs = h['binary_accuracy']
    # 验证精度
    validation_accs = h['val_binary_accuracy']

    plt.figure()
    plt.subplot(221)
    plt.plot(epochs, loss, label="train loss")
    plt.plot(epochs, validation_loss, label="validation_loss")
    plt.grid(True)
    plt.legend()
    ############################################################
    plt.subplot(222)
    plt.plot(epochs, accs, label="train acc")
    plt.plot(epochs, validation_accs, label="validation_accs")
    plt.grid(True)
    plt.legend()
    ############################################################
    plt.show()


if __name__ == "__main__":
    history_file = "./results/history_result1.pkl"
    train_x, train_y = load_haimo_data()
    main(history_file=history_file, x=train_x,y=train_y)
    plot(history_file)


