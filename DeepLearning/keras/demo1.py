"""
电影评论数据集模型
"""

from keras import models
from keras import layers
from keras import optimizers
from keras import activations
from keras import losses
from keras import metrics
from keras.regularizers import l1, l1_l2, l2
import numpy as np
import pickle


def demo():
    model = models.Sequential()
    model.add(layers.Dense(32, activation="relu", input_shape=(784,)))
    model.add(layers.Dense(10, activation="softmax"))

    print('ok')


# 加载数据
from keras.datasets import imdb

(train_data, train_labels), (test_data, test_labels) = imdb.load_data(num_words=10000)  #


def id2word(ids):
    word_index = imdb.get_word_index()
    reverse_word_index = dict([(index, word) for word, index in word_index.items()])
    # print(reverse_word_index)
    sentence = " ".join([reverse_word_index.get(i - 3, "?") for i in ids])
    return sentence


print("评论长度：", [len(i) for i in train_data])


def word2vector(sequences, dimension=10000):
    '''
    采用独热编码
    :param sequences: 数据集：行数
    :param dimension: 列数
    :return: np.array
    '''
    results = np.zeros(shape=(len(sequences), dimension))
    for i, sequence in enumerate(sequences):
        results[i, sequence] = 1
    return results


x_train = word2vector(train_data)
x_test = word2vector(test_data)
print(x_train[0])


def build_model_1():
    # 构建网络
    model = models.Sequential()
    model.add(layers.Dense(2000, activation="relu", input_shape=(10000,)))
    model.add(layers.Dense(1000, activation="relu"))
    model.add(layers.Dense(100, activation="relu"))
    model.add(layers.Dense(2, activation="binary_softmax"))
    # 构建损失函数


def __build_model_(partial_x_train, partial_y_train, x_val, y_val):
    """
    该模型表现不错
    :param partial_x_train:
    :param partial_y_train:
    :param x_val:
    :param y_val:
    :return:
    """
    # 构建网络
    model = models.Sequential()
    l_2 = l2(0.01) #L2 正则化
    # l_2 = l1_l2()
    model.add(layers.Dense(15, activation="relu", kernel_regularizer=l_2, input_shape=(10000,)))
    model.add(layers.Dense(60, kernel_regularizer=l_2, activation="relu"))
    model.add(layers.Dense(10, kernel_regularizer=l_2, activation="relu"))
    model.add(layers.Dense(1, activation=activations.sigmoid))
    # 构建损失函数,编译模型
    # model.compile(optimizer=optimizers.RMSprop(lr=0.001), loss=losses.binary_crossentropy, metrics=['accuracy'])
    model.compile(optimizer=optimizers.RMSprop(lr=0.001), loss=losses.binary_crossentropy,
                  metrics=[metrics.binary_accuracy])
    # 训练模型
    print("开始训练模型")
    import time
    start = time.time()
    history = model.fit(partial_x_train, partial_y_train, epochs=20, batch_size=512, validation_data=(x_val, y_val))
    end = time.time()
    t = (end - start) / 60
    print("训练耗时时间（分钟）：", str(t) )
    return history


def build_model_2(partial_x_train, partial_y_train, x_val, y_val, epochs=20):
    # 构建网络
    model = models.Sequential()
    l_2 = l2(0.01) #L2 正则化
    # l_2 = l1_l2()
    model.add(layers.Dense(15, activation="relu", kernel_regularizer=l_2, input_shape=(10000,)))
    model.add(layers.Dense(60, kernel_regularizer=l_2, activation="relu"))
    model.add(layers.Dense(10, kernel_regularizer=l_2, activation="relu"))
    model.add(layers.Dense(1, activation=activations.sigmoid))
    # 构建损失函数,编译模型
    # model.compile(optimizer=optimizers.RMSprop(lr=0.001), loss=losses.binary_crossentropy, metrics=['accuracy'])
    model.compile(optimizer=optimizers.RMSprop(lr=0.001), loss=losses.binary_crossentropy,
                  metrics=[metrics.binary_accuracy])
    # 训练模型
    print("开始训练模型")
    import time
    start = time.time()
    history = model.fit(partial_x_train, partial_y_train, epochs=epochs, batch_size=512, validation_data=(x_val, y_val))
    end = time.time()
    t = (end - start) / 60
    print("训练耗时时间（分钟）：", str(t) )
    return history, model


def main():
    y_train = train_labels
    # 验证集
    split_data = 10000
    x_val = x_train[:split_data]
    partial_x_train = x_train[split_data:]
    y_val = y_train[:split_data]
    partial_y_train = y_train[split_data:]

    history_file = "./results/history_result.pkl"
    history, model = build_model_2(partial_x_train=partial_x_train, partial_y_train=partial_y_train, x_val=x_val, y_val=y_val, epochs=4)
    # 历史数据保存
    pickle.dump(history, open(file=history_file, mode='wb'))
    # 测试 # 评估模型,不输出预测结果
    res = model.evaluate(x=x_test, y=test_labels) #(loss, acc)
    print(res)

if __name__ == "__main__":
    main()

if __name__ == "__main1__":
    main()
    history_file0 = "./results/history_0.pkl"
    history = pickle.load(open(history_file0, mode="rb"))
    h = history.history
    # 训练损失
    loss = h['loss']
    # 验证损失
    validation_loss = h['val_loss']
    # 训练批次
    epochs = range(1, 21)
    # 训练精度
    accs = h['binary_accuracy']
    # 验证精度
    validation_accs = h['val_binary_accuracy']
    import matplotlib.pyplot as plt
    plt.figure()
    plt.subplot(221)
    plt.plot(epochs, loss, label = "train loss")
    plt.plot(epochs, validation_loss, label = "validation_loss")
    plt.grid(True)
    plt.legend()
    ############################################################
    plt.subplot(222)
    plt.plot(epochs, accs, label = "train acc")
    plt.plot(epochs, validation_accs, label = "validation_accs")
    plt.grid(True)
    plt.legend()
    ############################################################
    history_file1 = "./results/history_1.pkl"
    history = pickle.load(open(history_file1, mode="rb"))
    h = history.history
    # 训练损失
    loss = h['loss']
    # 验证损失
    validation_loss = h['val_loss']
    # 训练批次
    epochs = range(1, 21)
    # 训练精度
    accs = h['binary_accuracy']
    # 验证精度
    validation_accs = h['val_binary_accuracy']
    ##################################################################
    plt.subplot(223)
    plt.plot(epochs, loss, label = "1 times train loss")
    plt.plot(epochs, validation_loss, label = "1 times validation_loss")
    plt.grid(True)
    plt.legend()
    ###################################################################
    plt.subplot(224)
    plt.plot(epochs, accs, label = "1 times train acc")
    plt.plot(epochs, validation_accs, label = "1 times validation_accs")
    plt.grid(True)
    plt.legend()
    ####################################################################
    ############################################################
    history_file = "./results/history_2.pkl"
    history = pickle.load(open(history_file, mode="rb"))
    h = history.history
    # 训练损失
    loss = h['loss']
    # 验证损失
    validation_loss = h['val_loss']
    # 训练批次
    epochs = range(1, 21)
    # 训练精度
    accs = h['binary_accuracy']
    # 验证精度
    validation_accs = h['val_binary_accuracy']
    ##################################################################
    plt.subplot(223)
    plt.plot(epochs, loss, "-.", label="3 times train loss")
    plt.plot(epochs, validation_loss, label="3 times validation_loss")
    plt.grid(True)
    plt.legend()
    ###################################################################
    plt.subplot(224)
    plt.plot(epochs, accs, "-.", label="3 times train acc")
    plt.plot(epochs, validation_accs, "-*", label="3 times validation_accs")
    plt.grid(True)
    plt.legend()

    plt.show()

