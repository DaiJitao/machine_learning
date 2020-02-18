""""""
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import jieba_fast as jieba
from pprint import pprint

s = ['机器学习', '表现', '不佳', '原因', '过度', '拟合', '欠', '拟合', '数据', '机器学习', '中', '逼近', '目标', '函数', '过程', '监督式机器学习', '理解', '逼近',
     '目标', '函数', 'f', 'f', '函数', '映射', '输入', '变量', 'X', '输出', '变量', 'Y', 'Y', 'f', 'X', 'Y', 'f', 'X', '特性', '描述', '用于',
     '定义', '分类', '预测', '机器学习', '算法', '领域']
# 统计词频
tf = CountVectorizer().fit_transform(s)
lda = LatentDirichletAllocation()
# Tf为得到各个文档的词频向量组成的列表
docres = lda.fit_transform(tf)

filepaths = ['./data/test1.txt', './data/test2.txt', './data/test3.txt', './data/test4.txt']
docs = [open(file, mode='r', encoding='utf-8').read() for file in filepaths]
# 分词
docs = [[word for word in jieba.lcut(doc)] for doc in docs]
# 去除停止词
stop_words_file = r"F:\pycharm_workspce\dai_github\myproject\machine_learning\data\StopWords.txt"
stop_words = set(open(stop_words_file, mode="r", encoding='utf-8').read().strip().split("\n"))
docs = [[word for word in doc if word not in stop_words] for doc in docs]

corpus = [" ".join(doc) for doc in docs]
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation

tfidf = TfidfVectorizer()
tfidf_matrix = tfidf.fit_transform(corpus)
pprint(corpus)
pprint(tfidf_matrix)

lda = LatentDirichletAllocation(n_topics=2, random_state=123456)
docres = lda.fit_transform(tfidf_matrix)
print(docres)
