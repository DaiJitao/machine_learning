from gensim.models.word2vec import Word2VecKeyedVectors

file = r"F:\NLP_learnings\词向量\腾讯中文词向量\Tencent_AILab_ChineseEmbedding.tar.gz"
wv_from_text = Word2VecKeyedVectors.load_word2vec_format(file, binary=False, encoding='gbk')
print(wv_from_text)