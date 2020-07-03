import os
import pandas as pd
from pyhanlp import HanLP
import jieba_fast as jieba

HanLP.Config.ShowTermNature = False  # 分词结果不展示词性


class TextOp(object):
    def __init__(self, stopwords_file=None):
        if stopwords_file:
            self.stopwords = set([line.rstrip() for line in open(stopwords_file)])
        else:
            self.stopwords = set()

    def cut_text(self):
        pass

    def clean_text(self):
        pass

    def remove_stopwords(self):
        pass

    def load_data(self, file):
        result = []
        with open(file, mode='r', encoding="utf-8") as fp:
            lines = fp.readlines()
            for line in lines:
                words = HanLP.segment(str(line).strip())
                result.append(" ".join([str(i.word) for i in words]))
        return result


def save_data():
    negdatafile = os.path.join(".", "data", "neg.csv")
    posdatafile = os.path.join(".", "data", "pos.csv")
    op = TextOp()

    negWords = op.load_data(negdatafile)
    newLabel = [0] * len(negWords)
    negDF = pd.DataFrame()
    negDF['words'] = negWords
    negDF['label'] = newLabel
    print(negDF.head())

    posWords = op.load_data(posdatafile)
    posLabel = [1] * len(posWords)
    posDF = pd.DataFrame()
    posDF['words'] = posWords
    posDF['label'] = posLabel
    print(posDF.head())

    # 保存
    negOutDataFile = os.path.join(".", "data", "negCutWords.csv")
    posOutDataFile = os.path.join(".", "data", "posCutWords.csv")
    negDF.to_csv(negOutDataFile, header=True, index=False)
    posDF.to_csv(posOutDataFile, header=True, index=False)

if __name__ == '__main__':
    save_data()

