from gensim.models import word2vec, Word2Vec
import time
import logging
import jieba_fast as jieba
import pymongo
import hashlib

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def load_data():
    s = "The official models are a collection of example models that use TensorFlow's high-level APIs. They are intended to " \
        "be well-maintained, tested, and kept up to date with the latest stable TensorFlow API. They should also be reasonably " \
        "optimized for fast performance while still being easy to read. We especially recommend newer TensorFlow users to start here."
    s = s.split(".")
    sentences = [t.split() for t in s]
    return sentences


sentences = load_data()
print(sentences)
# 构建模型
# min_count,频数阈值，大于等于1的保留
# size，神经网络 NN 层单元数，它也对应了训练算法的自由程度
# workers=4，default = 1 worker = no parallelization 只有在机器已安装 Cython 情况下才会起到作用。如没有 Cython，则只能单核运行。
# 默认值100层
# model = word2vec.Word2Vec(sentences=sentences, min_count=1) # min_count 一般设置为0-100之间，过滤掉低频词

# 加载已经训练好的词向量
model_file = ""
model = Word2Vec.load(model_file)
# 相近词
model.most_similar("微信")