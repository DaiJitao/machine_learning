
import os
from gensim.models import KeyedVectors

path = r"F:\NLP_learnings\词向量\腾讯中文词向量\Tencent_AILab_ChineseEmbedding"

file = os.path.join(path,"Tencent_AILab_ChineseEmbedding.txt")
wv_from_text = KeyedVectors.load_word2vec_format(file, binary=False) # 加载时间比较长

wv_from_text.init_sims(replace=True)

model = wv_from_text # 就是一个词向量模型
model.wv.similar_by_word('旅游', topn=100) # 和旅游相关的
word = '膝关节置换手术'
if word in wv_from_text.wv.vocab.keys():
    vec = wv_from_text[word]
    print(wv_from_text.most_similar(positive=[vec], topn=20))
else:
    print("没找到")