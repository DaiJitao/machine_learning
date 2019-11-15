""" 基于词向量的情感分析
https://blog.csdn.net/qq_33335484/article/details/82772549
https://github.com/freeingfree/lstm
 """

import jieba_fast as jieba
from gensim.models import word2vec, Word2Vec
import json
import re




class Word2VecModel():
    def __init__(self):
        pass

    def clean_data(self, file, outFile):
        with open(file, mode="r", encoding="utf-8") as f:
            doc = f.read()
            # print(doc)
            doc_cut = jieba.cut(doc)
            # print(" ".join(doc_cut))
            res = " ".join(doc_cut)

        with open(outFile, mode='w', encoding='utf-8') as f2:
            f2.write(res)

    def input_data(self, files):
        result = []
        for file in files:
            sentence = word2vec.LineSentence(file)
            result = result + [i for i in sentence]
        return result


    def train(self, sentence, save_model_file):
        # 创建词向量模型 由于语料库样本少 保留全部词汇进行训练
        model = Word2Vec(sentence, sg=1, size=256, window=5, min_count=1, negative=3, sample=0.001, hs=1,
                         workers=4)
        model.save(save_model_file)


if __name__ == '__main__':
    model = Word2VecModel()
    file_pos = "../data/pos.txt"
    file_pos_clean = "../data/clean_pos.txt"
    file_neg = "../data/neg.txt"
    file_neg_clean = "../data/clean_neg.txt"
    clean_data = False
    if clean_data:
        model.clean_data(file_pos, file_pos_clean)
        model.clean_data(file_neg, file_neg_clean)

    # result = model.input_data([file_neg_clean, file_pos_clean])
    # model.train(result, "../model/model_1.wv")
    model = Word2Vec.load("../model/model_1.wv")
    s = model.wv.most_similar("赞")
    t = model.wv.similarity("好用", "不错")
    print(s)
    print(t)

