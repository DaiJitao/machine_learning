from gensim.models import word2vec
import time
import logging
import jieba_fast as jieba

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

jieba.suggest_freq('沙瑞金', True)
jieba.suggest_freq('田国富', True)
jieba.suggest_freq('高育良', True)
jieba.suggest_freq('侯亮平', True)
jieba.suggest_freq('钟小艾', True)
jieba.suggest_freq('陈岩石', True)
jieba.suggest_freq('欧阳菁', True)
jieba.suggest_freq('易学习', True)
jieba.suggest_freq('王大路', True)
jieba.suggest_freq('蔡成功', True)
jieba.suggest_freq('孙连城', True)
jieba.suggest_freq('季昌明', True)
jieba.suggest_freq('丁义珍', True)
jieba.suggest_freq('郑西坡', True)
jieba.suggest_freq('赵东来', True)
jieba.suggest_freq('高小琴', True)
jieba.suggest_freq('赵瑞龙', True)
jieba.suggest_freq('林华华', True)
jieba.suggest_freq('陆亦可', True)
jieba.suggest_freq('刘新建', True)
jieba.suggest_freq('刘庆祝', True)
jieba.suggest_freq("京州市", True) # #True表示希望分出来，False表示不希望分出来。
jieba.suggest_freq("H省", True)
jieba.suggest_freq("副书记", True)


def clean_data(file, outFIle):
    with open(file, mode="r", encoding="utf-8") as f:
        doc = f.read()
        # print(doc)
        doc_cut = jieba.cut(doc)
        # print(" ".join(doc_cut))
        res = " ".join(doc_cut)
    with open(outFIle, mode='w', encoding='utf-8') as f2:
        f2.write(res)


def mode(file, modelFile):
    sentences = word2vec.Text8Corpus(file)
    model = word2vec.Word2Vec(sentences, sg=1, size=256, window=5, min_count=5, negative=3, sample=0.0005, hs=1,
                              workers=4)
    model.save(modelFile)
    print("训练完毕")
    return model


if __name__ == "__main__":
    file = r"F:\NLP_learnings\data\word2vec\chinese\in_the_name_of_people\in_the_name_of_people.txt"
    cleanData = r"F:\NLP_learnings\data\word2vec\chinese\in_the_name_of_people\cleaned2.txt"
    outmodel = r"F:\NLP_learnings\data\word2vec\chinese\in_the_name_of_people\model2"
    model_1 = r"E:\BaiduNetdiskDownload\实战-机器学习\word2vec\word2vec_c_from_weixin\word2vec_c"
    startTime = time.time()
    # model = mode(file, outModel)
    # endTime = time.time()
    # print("消费时间（分钟）：", (endTime-startTime) // 60 )
    # print(model['man'])
    # 清洗数据。分词
    # clean_data(file, cleanData)
    train = False
    if train:
        sentences = word2vec.LineSentence(cleanData)  # 使其格式化
        # workers参数用于设置并发训练时候的线程数，不过仅当Cython安装的情况下才会起作用
        # 模型保存和训练
        model = word2vec.Word2Vec(sentences, sg=0, size=256, window=8, min_count=20, negative=3, sample=0.001, hs=1,
                                  workers=4)
        model.save(outmodel)

    # 加载模型
    model = word2vec.Word2Vec.load(model_1)
    #
    # req_count = 5
    # for key in model.wv.similar_by_word('旅游', topn=100):
    #     if len(key[0]) == 3:
    #         req_count -= 1
    #         print(key[0], key[1])
    #         if req_count == 0:
    #             break
    #
    # print(model.wv.doesnt_match(u"沙瑞金 高育良 李达康 刘庆祝".split()))
    # print(model.most_similar("沙瑞金"))
    print(model.similarity("女人", "男人"))
    print(model.similarity("您好", "你好"))

