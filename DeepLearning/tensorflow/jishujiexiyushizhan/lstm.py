import tensorflow as tf
import tensorflow.models.tutorials.rnn.ptb.reader as reader

# 定义LSTM模型
class LSTM_Model():
    def __init__(self, embedding_size, rnn_size, batch_size, learning_rate,
                 training_seq_len, vocab_size, infer_sample=False):
        self.embedding_size = embedding_size
        self.rnn_size = rnn_size
        self.vocab_size = vocab_size
        self.infer_sample = infer_sample
        self.learning_rate = learning_rate

        if infer_sample:
            self.batch_size = 1
            self.training_seq_len = 1
        else:
            self.batch_size = batch_size
            self.training_seq_len = training_seq_len

        self.lstm_cell = tf.contrib.rnn.B

if __name__ == "__main__":
    file = "./data/pg100.txt"
    s_text = open(file, mode="r").read().strip()
    s_text = s_text.replace('\r\n', '')
    s_text = s_text.replace('\n', '')
    print(len(s_text))
    train, valid, test, _ = reader.ptb_raw_data("./data/ptb/")
    print(_)