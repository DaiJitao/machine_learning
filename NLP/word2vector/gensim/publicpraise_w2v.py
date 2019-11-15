"""构建口碑词向量

"""

from gensim.models import word2vec, Word2Vec
import time
import logging
import jieba_fast as jieba
import json
import re
import os

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# centfile = r"F:\pycharm_workspce\myML_DM_Test\src\NLP\word2vector\gensim\cent.txt"


def load_files(path):
    pass


class PublicPraise():
    def __init__(self):
        pass

    def clean_data(self, files, out_file):
        """ 清晰口碑数据 """
        file_out = open(out_file, mode="w+", encoding="utf-8")
        count = 0
        for file in files:
            try:
                with open(file, mode='r', encoding="utf-8") as contens:
                    for line in contens.readlines():
                        content = json.loads(line)['content'].strip()
                        # print(content)
                        res = re.sub(
                            '''http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+''', '',
                            content)
                        res = res = re.sub("[▽∩╭╮（￣▽￣）/丶⚠♑//@C3////#￠θм🧣📎❤|]", " ", res)
                        res = re.sub(r'<.*?>', '', res)
                        res = res.replace(" ", "").replace("\t", "").strip()
                        # print(res)
                        if len(res) >= 2:
                            file_out.write(res)
                        count += 1
                        if count % 2000 == 0:
                            print("写入： ", count)
                            file_out.flush()
            except Exception as e:
                print(e)
        file_out.close()

    def cut_data(self, file, out_file):
        file_data = open(file, mode="r", encoding="utf-8")
        out_data = open(out_file, mode="w+", encoding="utf-8")
        try:
            count = 0
            for data in file_data.readlines():
                temp = data.strip()
                res = jieba.cut(temp)
                res = " ".join(res)
                out_data.write(res)
                count += 1
                if count % 1000 == 0:
                    print("写入", count)
                    out_data.flush()
            file_data.close()
            out_data.close()
        except Exception as e:
            print(e)
            file_data.close()
            out_data.close()


def getCentWOrds(file):
    s = set()
    with open(file, mode="r", encoding="utf-8") as file1:
        for line in file1.readlines():
            temp = line.strip().split("\t")
            if len(temp[0].strip()) != 0:
                s.add(temp[0])
    return s

class Word2VecModel():
    def __init__(self):
        pass

    def input_data(self, files):
        """格式化数据"""
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
    cleaned_file = "./cleaned_data/cleaned.txt"
    cut_file = "./cleaned_data/cut_words.txt"
    filePath = './data/taskDir/'
    save_model_file = "./model/model_1.w2v"  # 模型保存路径
    if False:
        # 清洗数据
        # files = os.listdir(filePath)
        # files = [filePath + name for name in files if "cleaned" not in name]
        praise = PublicPraise()
        #print(files[:1000])
        #praise.clean_data(files[:1000], cleaned_file)
        print("清洗完毕,开始分词...")
        praise.cut_data(cleaned_file, cut_file)
        print("分词完毕！")

    if True:
        # 训练词向量
        model = Word2VecModel()
        sentences = word2vec.LineSentence(cut_file) # model.input_data(files=[cut_file])
        print("数据格式化成功： ", sentences)
        model.train(sentences, save_model_file=save_model_file)
        print("保存成功！", save_model_file)

    if False:
        model = Word2Vec.load(save_model_file)
        s = model.most_similar("法拉利")
        print(s)
