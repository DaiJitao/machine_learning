"""
疫情期间网民情绪识别
"""

import numpy as np
import jieba_fast as jieba
import pandas as pd
import re

def load_data(file):
    data_df = pd.read_csv(file, encoding='utf-8')
    content = data_df['微博中文内容']
    label = data_df['情感倾向']
    content_cleaned = content.apply(clean_text)
    count = 0
    new_df = pd.DataFrame({"原文":content, "清洗":content_cleaned})
    new_df.to_csv(r"F:\NLP_learnings\data\dataFountain\train_ dataset\clean_test.csv",encoding='utf-8',index=False)





def cut_words(text):
    jieba.cut

def clean_text(text):
    text = str(text)
    # 去掉url地址
    text = re.sub('''http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+''', '', text)
    # 去掉@某某某
    text = re.sub('''@.+@.+([\n]|[\t])''', '', text)
    text = re.sub("@|//@|～|>{1,}|\(\)", " ", text)
    # 多个问号变为一个问号
    text = re.sub(r"[。？\?]{2,}", "？", text)
    text = re.sub(r"！{2,}", "！", text)
    # 去掉#某某某# 和单个字母单个数字
    text = re.sub("#.{1,6}#|展开全文|([a-zA-Z]|[0-9])", "", text)
    # ？? -> ?
    text = re.sub(r"(\?？)|(？\?)", "？",text)
    text = re.sub(r"—{2,}|-{2,}", "—", text)
    text = re.sub(r"…{1,}|\.{4,}", "…", text)
    r = u'[/【】●■�→．・９８７６５４３２１０／％［］×\[\]^_`{|}~(:з」∠)]'
    text = re.sub(r, " ", text)

    # 去掉特殊标点符号
    # r = u'[!"#$%&\'()*+,-./:;<=>《￥★▼》，。·“”（）、；：？【】—！●■�0123456789．・９８７６５４３２１０／％［］×…?@[\\]^_`{|}~]'
    # text = re.sub(r, '', text)
    return text

if __name__ == '__main__':
    file_train_csv = r"F:\NLP_learnings\data\dataFountain\train_ dataset\nCoV_100k_train.labled.csv"
    load_data(file=file_train_csv)

    c = '新年第一天，为自己鼓掌??????发烧了也要来看线下演出！因为热爱，所以才会克服困难线上演出太炸了，爱呼兰，爱赵晓卉长这么大第一次这么近距离看到“明星”哈哈哈哈～新的一年，希望自己更要勇敢，更要坚强，坚持自己，坚持自己思想，坚持内心想法最后新?展开全文c'
    print(c)
    text = re.sub(r"\?{2,}", "?", c)
    print(text)