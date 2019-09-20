from gensim.models import word2vec
import time
import logging
import jieba_fast as jieba

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

centfile = r"F:\pycharm_workspce\myML_DM_Test\src\NLP\word2vector\gensim\cent.txt"


def getCentWOrds(file):
    s = set()
    with open(file, mode="r", encoding="utf-8") as file1:
        for line in file1.readlines():
            temp = line.strip().split("\t")
            if len(temp[0].strip()) != 0:
                s.add(temp[0])
    return s


# 添加中心词
for word in getCentWOrds(centfile):
    jieba.suggest_freq(word, True)


def clean_data(file, outFIle):
    with open(file, mode="r", encoding="utf-8") as f:
        doc = f.read()
        # print(doc)
        doc_cut = jieba.cut(doc)
        # print(" ".join(doc_cut))
        res = " ".join(doc_cut)
    with open(outFIle, mode='w', encoding='utf-8') as f2:
        f2.write(res)
