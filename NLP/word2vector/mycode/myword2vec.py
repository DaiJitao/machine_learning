import os
import os
import numpy as np
import zipfile
import collections
import random
import tensorflow as tf

# http://mattmahoney.net/dc/textdata.html
dataset_link = 'http://mattmahoney.net/dc/text8.zip'
zip_file = 'text8.zip'


def read_data(text8):
    with open(text8, encoding='utf-8', mode='r') as fp:
        return fp.read().strip()


def text_processing(ft8_text):
    '''
    # 标点处理
    :param ft8_text:
    :return:  转换为列表
    '''
    ft8_text = ft8_text.lower()
    ft8_text = ft8_text.replace('.', ' <period> ')
    ft8_text = ft8_text.replace(',', ' <comma> ')
    ft8_text = ft8_text.replace('"', ' <quotation> ')
    ft8_text = ft8_text.replace(';', ' <semicolon> ')
    ft8_text = ft8_text.replace('!', ' <exclamation> ')
    ft8_text = ft8_text.replace('?', ' <question> ')
    ft8_text = ft8_text.replace('(', ' <paren_l> ')
    ft8_text = ft8_text.replace(')', ' <paren_r> ')
    ft8_text = ft8_text.replace('--', ' <hyphen> ')
    ft8_text = ft8_text.replace(':', ' <colon> ')
    ft8_text_tokens = ft8_text.split()
    return ft8_text_tokens  # 转换为列表


def remove_lowerfreword(ft_tokens, fre=7):
    '''去除与单词相关的噪音：输入数据集中词频小于7的单词
    '''
    word_cnt = collections.Counter(ft_tokens)  # 统计列表元素出现次数,一个无序的容器类型，以字典的键值对形式存储,其中元素作为key，其计数作为value
    shortlisted_words = [w for w in ft_tokens if word_cnt[w] > fre]
    # print(shortlisted_words[:15])  # 列出数据集中词频最高的15个单词
    # print('Total number of shortlisted_words', len(shortlisted_words))  # 16616688
    # print('Unique number of shortlisted_words', len(set(shortlisted_words)))  # 53721
    return shortlisted_words


def dict_creation(shortlisted_words):
    '''创建词汇表：单词-id'''
    counts = collections.Counter(shortlisted_words)
    vocabulary = sorted(counts, key=counts.get, reverse=True)
    rev_dictionary = {ii: word for ii, word in enumerate(vocabulary)}  # 整数:单词
    dictionary = {word: ii for ii, word in rev_dictionary.items()}  # 单词:整数
    return dictionary, rev_dictionary


def subsampling(words_cnt):
    # 采用子采样处理文本中的停止词
    thresh = 0.00005
    word_counts = collections.Counter(words_cnt)
    total_count = len(words_cnt)
    freqs = {word: count / total_count for word, count in word_counts.items()}
    p_drop = {word: 1 - np.sqrt(thresh / freqs[word]) for word in word_counts}
    train_words = [word for word in words_cnt if p_drop[word] < random.random()]
    return train_words


def skipG_target_set_generation(batch_, batch_index, word_window):
    # 以所需格式创建skip-gram模型的输入：即中心词周围的词
    random_num = np.random.randint(1, word_window + 1)  # 在word_window范围内随机选取周围词的数量
    words_start = batch_index - random_num if (batch_index - random_num) > 0 else 0
    words_stop = batch_index + random_num
    window_target = set(batch_[words_start:batch_index] + batch_[batch_index + 1:words_stop + 1])
    return list(window_target)


def skipG_batch_creation(short_words, batch_length, word_window):
    # 创建中心词及其周围单词的组合形式
    batch_cnt = len(short_words) // batch_length
    print('batch_cnt=', batch_cnt)
    short_words = short_words[:batch_cnt * batch_length]

    for word_index in range(0, len(short_words), batch_length):
        input_words, label_words = [], []
        word_batch = short_words[word_index:word_index + batch_length]

        for index_ in range(len(word_batch)):  # 遍历每个batch中的每个中词
            batch_input = word_batch[index_]
            batch_label = skipG_target_set_generation(word_batch, index_, word_window)  # 获取周围单词
            label_words.extend(batch_label)
            input_words.extend([batch_input] * len(batch_label))  # skip_gram的输入形式，周围单词都得对应上中心词
            yield input_words, label_words


def main():
    tf_graph = tf.Graph()
    with tf_graph.as_default():
        intput_ = tf.placeholder(dtype=tf.int32, shape=[None], name="input_")
        label_ = tf.placeholder(dtype=tf.int32, shape=[None, None], name="label_")

    # 2. 得到embedding
    with tf_graph.as_default():
        word_embed = tf.Variable(tf.random_uniform((len(rev_dictionary), 300), -1, 1))
        embedding = tf.nn.embedding_lookup(word_embed, intput_)  # 将单词转换为向量


batch_length = 10
word_window = 5

if __name__ == '__main__':
    file = './data/text8'
    full_text = read_data(file)
    ft_tokens = text_processing(full_text)  # 单词列表
    shortlisted_words = remove_lowerfreword(ft_tokens, fre=0)  # 删除低频词
    dictionary, rev_dictionary = dict_creation(shortlisted_words)  # 字典和单词ID rev_dictionary={"0"=单词}；dictionary={"单词"=0}
    print(rev_dictionary.get(5233), rev_dictionary.get(3080), rev_dictionary.get(194))
    print(shortlisted_words[:100])
    words_cnt = [dictionary[word] for word in shortlisted_words]  # 通过词典获取每个单词对应的整数
    print('通过词典获取每个单词对应的整数')
    train_words = subsampling(words_cnt)
    print('train_words=', train_words[:100])  #
    batches = skipG_batch_creation(train_words, batch_length, word_window)
    i = 0
    for x, labels in batches:
        print("i={}, x={}, \n     labels={}".format(i, x, labels))
        if i == 11:
            break
        i += 1

