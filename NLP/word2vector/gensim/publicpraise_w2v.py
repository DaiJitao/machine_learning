"""构建口碑词向量

"""

from gensim.models import word2vec, Word2Vec
import time
import logging
import jieba
# import jieba_fast as jieba
import json
import re
import os

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# centfile = r"F:\pycharm_workspce\myML_DM_Test\src\NLP\word2vector\gensim\cent.txt"


jieba.suggest_freq("行车灯", True)


# 停用词 之外


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
                        # res = res = re.sub("[▽【∩╭╮（￣▽￣）🇨🇳♥️/丶⚠♑//@C3////#￠θ🤭🧡🔗м🧣📎❤】|]", " ", res)
                        res = re.sub(r'<.*?>', '', res)
                        # 去掉表情:以中括号括起来[开心]
                        res = re.sub('''\[([^\[\]]+)\]''', '', res)
                        # 去掉@某某某
                        res = re.sub('''@.+@.+([\n]|[\t])''', '', res)
                        res = re.sub(r"([a-zA-Z\d]){8,}", "", res)  # 8个字符以上的英文 ([^\u4e00-\u9fa5a-zA-Z\d])
                        res = re.sub(r"([^\u4e00-\u9fa5a-zA-Z\d])", "", res)  # 去除特殊符号

                        if len(res) >= 2:
                            res = re.sub(r"([a-zA-Z\d]){8,}", "", res)  # 8个字符以上的英文 ([^\u4e00-\u9fa5a-zA-Z\d])
                            res = re.sub(r"([^\u4e00-\u9fa5a-zA-Z\d])", "", res)  # 去除特殊符号
                            file_out.write(res + "\n")
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
                temp = re.sub(r"[a-zA-Z\d]{8,}", "", temp)
                if len(temp) < 2:
                    continue
                res = jieba.cut(temp)
                res = " ".join(res)
                out_data.write(res + "\n")
                count += 1
                if count % 5000 == 0:
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

def window_demo():
    cleaned_file = r'C:\Users\dell\Desktop\praise_w2c\cleaned_data\cleaned_1.txt'
    cut_file = r'C:\Users\dell\Desktop\praise_w2c\cleaned_data\cut_words1.txt'
    data_path = r'C:\Users\dell\Desktop\praise_w2c\data\\'
    save_model_file = "../model/model_1.w2v"  # 模型保存路径

    if True:
        # 清洗数据
        files = os.listdir(data_path)
        files = [data_path + name for name in files]
        praise = PublicPraise()
        # print(files[3000:5000])
        # files = files[4000:8000]
        # praise.clean_data(files, cleaned_file)
        print("清洗完毕,开始分词...")
        praise.cut_data(cleaned_file, cut_file)
        print("分词完毕！")

    if False:
        # 训练词向量
        model = Word2VecModel()
        sentences = word2vec.LineSentence(cut_file)  # model.input_data(files=[cut_file])
        print("数据格式化成功： ", sentences)
        model.train(sentences, save_model_file=save_model_file)
        print("保存成功！", save_model_file)

    if False:
        model = Word2Vec.load(save_model_file)
        s = model.most_similar("宾利")
        print(s)


def linux_res():
    cleaned_file = './cleaned_data/cleaned1.txt'
    cut_file = './cleaned_data/cut_words1.txt'
    data_path = './data/taskDir/'
    save_model_file = "./model/model_1.w2v"  # 模型保存路径

    if True:
        # 清洗数据
        files = os.listdir(data_path)
        files = [data_path + name for name in files]
        praise = PublicPraise()
        print(files[8000])
        files = files[4000:8000]
        praise.clean_data(files, cleaned_file)
        print("清洗完毕,开始分词...")
        praise.cut_data(cleaned_file, cut_file)
        print("分词完毕！")

    if False:
        # 训练词向量
        model = Word2VecModel()
        sentences = word2vec.LineSentence(cut_file)  # model.input_data(files=[cut_file])
        print("数据格式化成功： ", sentences)
        model.train(sentences, save_model_file=save_model_file)
        print("保存成功！", save_model_file)

    if False:
        model = Word2Vec.load(save_model_file)
        s = model.most_similar("宾利")
        print(s)

if __name__ == '__main__':
    linux_res()
    # window_demo()

