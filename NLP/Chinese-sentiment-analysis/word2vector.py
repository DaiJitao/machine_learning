from gensim.models import Word2Vec
import multiprocessing
import os
import pandas as pd
import numpy as np
import re
from pprint import pprint

"""
用于训练词向量
"""

negOutDataFile = os.path.join(".", "data", "negCutWords.csv")
posOutDataFile = os.path.join(".", "data", "posCutWords.csv")


'''
LineSentence(inp)：格式简单：一句话=一行; 单词已经过预处理并被空格分隔。
size：是每个词的向量维度； 
window：是词向量训练时的上下文扫描窗口大小，窗口为5就是考虑前5个词和后5个词； 
min-count：设置最低频率，默认是5，如果一个词语在文档中出现的次数小于5，那么就会丢弃； 
workers：是训练的进程数（需要更精准的解释，请指正），默认是当前运行机器的处理器核数。这些参数先记住就可以了。
sg ({0, 1}, optional) – 模型的训练算法: 1: skip-gram; 0: CBOW
alpha (float, optional) – 初始学习率
iter (int, optional) – 迭代次数，默认为5
'''


def removed_numbers(words):
    """
    删除数字
    :param word:
    :return:
    """
    if type(words) == type(""):
        words = re.sub(r"-{0,1}\d{1,}", "", words)
        return words
    else:
        return ""




isTrain = False # 是否训练词向量
isTest = True # 词向量的测试
saveModel = "./models/gensim_CBOW_w2v.model"

if isTrain:
    negwords = pd.read_csv(negOutDataFile)
    poswords = pd.read_csv(posOutDataFile)

    sentences = negwords['words'].tolist() + poswords['words'].tolist()
    sentences = [removed_numbers(words) for words in sentences]
    sentences = [s.split(" ") for s in sentences]
    print(sentences[:6])
    model = Word2Vec(sentences, size=512, sg=0, window=5, min_count=5, workers=multiprocessing.cpu_count())
    model.save(saveModel)
    print("模型已经保存："+saveModel)

if isTest:
    # 加载模型
    model = Word2Vec.load(saveModel)
    pprint(model.wv.most_similar("北京"))

    pprint(model['北京'])

