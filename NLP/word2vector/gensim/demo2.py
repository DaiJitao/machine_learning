from gensim.models import word2vec
import numpy as np


def euDistant(word1, word2):
    if len(word1) != len(word2):
        raise Exception("维度不一致")

    sum_ = 0
    for (x, y) in zip(word1, word2):
        sum_ = sum_ + np.square((x - y))

    return np.sqrt(sum_)


if __name__ == "__main__":
    modelFile1 = r"F:\NLP_learnings\data\word2vec\text8\out200.model1"
    modelFile2 = r"F:\NLP_learnings\data\word2vec\text8\out200.model2"
    model1 = word2vec.Word2Vec.load(modelFile1)
    model2 = word2vec.Word2Vec.load(modelFile2)
    man = model1.wv.get_vector("man")
    # man2 = model2["man"]
    love = model1.wv.get_vector("love")
    loved = model1.wv.get_vector("loved")
    print(model1.wv.get_vector("man"))
    print(euDistant(man, love))
    print(euDistant(love, loved))
