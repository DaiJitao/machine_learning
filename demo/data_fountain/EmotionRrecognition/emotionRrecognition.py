"""
疫情期间网民情绪识别
"""

import numpy as np
import jieba
import pandas as pd
import re

jieba.load_userdict("./data/user_dict.txt")


def clean_data(file, out_csv):
    data_df = pd.read_csv(file, encoding='utf-8')
    content = data_df['微博中文内容']
    label = data_df['情感倾向']
    content_cleaned = content.apply(clean_text)
    new_df = pd.DataFrame({"微博中文内容": content, "清洗后内容": content_cleaned, "情感倾向": label})
    new_df.to_csv(out_csv, encoding='utf-8', index=False)


def clean_text(text):
    text = str(text)
    # 去掉url地址
    text = re.sub('''http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+''', '', text)
    # 去掉@某某某
    text = re.sub('''@.+@.+([\n]|[\t])''', '', text)
    text = re.sub("//@|～|>{1,}|\(\)|[@·『』]", " ", text)
    # 多个问号变为一个问号
    text = re.sub(r"[。？\?]{2,}", "？", text)
    text = re.sub(r"！{2,}", "！", text)
    # 去掉#某某某# 和单个字母单个数字
    text = re.sub("#.{1,6}#|展开全文|([a-zA-Z]|[0-9])", "", text)
    # ？? -> ?
    text = re.sub(r"(\?？)|(？\?)", "？", text)
    text = re.sub(r"—{2,}|-{2,}", "—", text)
    text = re.sub(r"…{1,}|\.{4,}", "…", text)
    r = u'[/【】●■�→．・（９８７６５４３２１０／％［］×\[\]^_`{|}~(:з」∠)）①②③④]|(#|↓|(-  -)){1,}'
    text = re.sub(r, " ", text)

    # 去掉特殊标点符号
    # r = u'[!"#$%&\'()*+,-./:;<=>《￥★▼》，。·“”（）、；：？【】—！●■�0123456789．・９８７６５４３２１０／％［］×…?@[\\]^_`{|}~]'
    # text = re.sub(r, '', text)
    return text


def stop_word(file):
    with open(file, encoding="utf-8", mode="r") as f:
        d = f.read()
        stopWords = set(d.split("\n"))
    return list(stopWords)


def remove_word(src_word, stop_word):
    '''
    去除停用词
    :param src_word:
    :param stop_word:
    :return:
    '''
    return [word for word in src_word if word not in stop_word]


def cut_words(text):
    text = str(text).strip()
    text = re.sub("\ue627", "", text)
    text = re.sub(r"[★☆]{1,}", "", text)
    if len(text) == 0 or len(text) == 1:
        return text
    cut_word = jieba.cut(text)
    src_word = [word for word in cut_word if len(word.strip()) > 0]
    words = remove_word(src_word, stop_word)
    text = " ".join(words)
    return text


def cut_data(file, out_csv):
    data_df = pd.read_csv(file, encoding='utf-8')
    content = data_df['清洗后内容']
    label = data_df['情感倾向']
    cut_content = content.apply(cut_words)
    new_df = pd.DataFrame({"分词": cut_content, "情感倾向": label})
    new_df.to_csv(out_csv, encoding='utf-8', index=False)


def get_fastText_data(train_data, out_file):
    data_df = pd.read_csv(train_data, encoding='utf-8')
    cut_content = data_df["分词"]
    label = data_df['情感倾向']
    with open(out_file, mode='a', encoding='utf-8') as file:
        for words, cls in zip(cut_content, label):
            words = str(words).strip()
            cls = str(cls).strip()
            line = "__label__" + str(cls) + " " + words + "\n"
            file.write(line)
    print("数据处理完毕！")

def split_data_train_test(data_file, rows, out_train_file, out_test_file, split_rate=0.8 ):
    """

    :param data_file:
    :param out_train_file:
    :param rows: 数据集总行数
    :param out_test_file:
    :param split_rate: 数据划分比例；0.8代表百分之八十训练集
    :return:
    """
    index = int(rows * split_rate)
    out_train_data = open(out_train_file, encoding='utf-8', mode='a+')
    out_test_data = open(out_test_file, mode="a+", encoding="utf-8")
    with open(data_file, mode='r', encoding="utf-8") as file:
        lines = file.readlines()
        i = 0
        for line in lines:
            if i < index:
                out_train_data.write(line + "\n")
            else:
                out_test_data.write(line + "\n")
            i += 1
    out_test_data.close()
    out_train_data.close()





if __name__ == '__main__':
    base_dir = r"F:\NLP\报名比赛\疫情期间网民情绪识别\train_ dataset"
    file_train_csv = base_dir + r"\nCoV_100k_train.labled.csv"
    file_train_cleaned_csv = base_dir + r"\cleaned_nCoV_100k_train.labled.csv"
    file_train_cut_csv = base_dir + r"\cutOK_nCoV_100k_train.labled.csv"
    # load_data(file=file_train_csv, out_csv=file_train_cleaned_csv)
    # stop_word_file = r"F:\pycharm_workspace\mygithub\machine_learning\data\StopWords.txt"
    # stop_word = stop_word(stop_word_file)
    # cut_data(file_train_cleaned_csv, file_train_cut_csv)
    train_data = file_train_cut_csv
    out_file = base_dir + r"\train_data_all.txt"
    # get_fastText_data(train_data, out_file)
    split_data_train_test(data_file=out_file, rows=100000, out_train_file=base_dir+r"\train_data.txt", out_test_file=base_dir + r"\test_data.txt")

