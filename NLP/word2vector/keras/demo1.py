from keras.datasets import imdb
from keras.models import Sequential
from keras.layers import Dense, Embedding, Flatten
from keras import activations
from keras import optimizers
from keras import losses
from keras import metrics
import keras.preprocessing as preprocessing

max_features = 10000
maxlen = 20

(x_train, y_train), (x_test, y_test) = imdb.load_data(num_words=max_features)
x_train = preprocessing.sequence.pad_sequences(x_train, maxlen=maxlen)
x_test = preprocessing.sequence.pad_sequences(x_test, maxlen=maxlen)
print(len(x_train))
print(len(x_train[0]))

# 建立模型
model = Sequential()
model.add(Embedding(10000, 8 , input_length=maxlen))
model.add(Flatten())
model.add(Dense(1, activation=activations.sigmoid))
model.compile(optimizer=optimizers.RMSprop(lr=0.001), loss=losses.binary_crossentropy, metrics=[metrics.binary_accuracy])
model.summary()
history = model.fit(x_train, y_train, epochs=20, batch_size=32, validation_split=.2)
