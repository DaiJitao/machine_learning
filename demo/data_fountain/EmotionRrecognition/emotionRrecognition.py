"""
疫情期间网民情绪识别
"""

import numpy as np
import jieba_fast as jieba
import pandas as pd
import re
import json


def load_data(file):
    data_df = pd.read_csv(file, encoding='utf-8')
    content = data_df['微博中文内容']
    label = data_df['情感倾向']
    content_cleaned = content.apply(clean_text)
    count = 0
    new_df = pd.DataFrame({"原文": content, "清洗": content_cleaned})
    new_df.to_csv(r"F:\NLP_learnings\data\dataFountain\train_ dataset\clean_test.csv", encoding='utf-8', index=False)


def cut_words(text):
    jieba.cut


def clean_text(text):
    text = str(text)
    # 去掉url地址
    text = re.sub('''http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+''', '', text)
    # 去掉@某某某
    text = re.sub('''@.+@.+([\n]|[\t])''', '', text)
    # text = re.sub("(、，)|@|//@|～|>{1,}|\(\)", "，", text)
    text = re.sub("[(。，)(！，)(？，)(、，)@(//@)～>\(\)]{1,}", "，", text)
    # 多个问号变为一个问号
    text = re.sub(r"[。？\?]{2,}", "？", text)
    text = re.sub(r"[！!]{2,}", "！", text)
    # 去掉#某某某# 和单个字母单个数字
    text = re.sub("转发微博|#.{1,6}#|展开全文|([a-zA-Z]|[0-9])", "", text)
    # ？? -> ?
    text = re.sub(r"(\?？)|(？\?)", "？", text)
    text = re.sub(r"—{2,}|-{2,}", "—", text)
    text = re.sub(r"…{1,}|\.{4,}", "…", text)
    r = u'[/【】●■�→．・🇨🇳９８７６５４３２１０／％［］×\[\]^_`{|}~(:з」∠)]'
    text = re.sub(r, "，", text)
    # 去掉非中文
    not_chinese = r'[^\u4e00-\u9fa5，{}【】（）。：；“‘”…《》、！？——]'
    text = re.sub(not_chinese, " ", text)
    # 多个空格变为1个
    text = re.sub(r"\s{1,}", " ", text)
    text = re.sub(r"[(\s，)(\s,),，(（）)(：，)(： ：)]{1,}", "，", text).strip()
    return text


if __name__ == '__main__':
    # file_train_csv = r"F:\NLP_learnings\data\dataFountain\train_ dataset\nCoV_100k_train.labled.csv"
    # load_data(file=file_train_csv)

    file = r"F:\pycharm_workspce\dai_github\ml_test1\machine_learning\demo\data_fountain\data\hotworddata2.txt"
    with open(file=file, mode='r', encoding='utf-8') as fp:
        for line in fp.readlines():
            d = json.loads(line)['content']
            print(d)
            print("-->")
            print(clean_text(d))
            print("\n\n\n")

