import jieba_fast as jieba

jieba.suggest_freq('沙瑞金', True)
jieba.suggest_freq('易学习', True)
jieba.suggest_freq('王大路', True)
jieba.suggest_freq('京州', True)
jieba.suggest_freq('桓温', True)


def cut(file, outfile):
    with open(file, mode='r', encoding="utf-8") as f:
        document = f.read()
        document_cut = jieba.cut(document)
        result = ' '.join(document_cut)
        with open(outfile, mode='w', encoding="utf-8") as outF:
            outF.write(result)

    print("文件已分词！")


'''分词'''


# cut("./data/nlp_test0.txt", "./data/nlp_cut0.txt")
# cut("./data/nlp_test1.txt", "./data/nlp_cut1.txt")
# cut("./data/nlp_test2.txt", "./data/nlp_cut2.txt")

def loadCorpus(files):
    res = []
    for file in files:
        with open(file, mode='r', encoding='utf-8') as f:
            res.append(f.read().strip())
    return res


'''导入停用词表'''
stopWordsFile = "./data/StopWords.txt"
stpwrd_dic = open(stopWordsFile, mode='r', encoding='utf-8')
stpwrd_content = stpwrd_dic.read()
# 将停用词表转换为list
stopWords = stpwrd_content.splitlines()
stpwrd_dic.close()

# 导入统计词频工具
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation as LDA

files = ["./data/nlp_cut0.txt", "./data/nlp_cut1.txt", "./data/nlp_cut2.txt"]
corpus = loadCorpus(files)
'''去除停用词'''
cntVector = CountVectorizer(stopWords)
cntTf = cntVector.fit_transform(corpus)
print(cntTf)

lda = LDA(n_topics=2, learning_offset=50., random_state=0)
docres = lda.fit_transform(cntTf)

print(docres)
print(docres.shape) # (文档数，主题数）
print(lda.components_)
