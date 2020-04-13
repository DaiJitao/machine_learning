from fasttext import train_supervised
from fasttext import train_supervised
from fasttext import load_model
# Skipgram model :
# model = fasttext.train_unsupervised('data.txt', model='skipgram')
#
# # or, cbow model :
# model = fasttext.train_unsupervised('data.txt', model='cbow')

def tain_model(train_file):
    model = train_supervised(input=train_file, epoch=10, lr=0.1, wordNgrams=2, minCount=1, loss="softmax")





if __name__ == '__main__':
    base_dir = r"F:\NLP\报名比赛\疫情期间网民情绪识别\train_dataset"
    train_file = "./data/train_data.txt"
    test_file = "./data/test_data.txt"

    classifier = train_supervised(train_file, label='__label__', dim=100, epoch=20,
                                           lr=.1, wordNgrams=2, loss="softmax")
    #
    classifier.save_model("./train.model4")
    for i in range(4):
        cls = load_model("./models/train.model"+ str(i+1))
        # 整体的结果为(测试数据量，precision，recall)：
        print(str(i+1) + " ", classifier.test(test_file))


