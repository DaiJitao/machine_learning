# map tag to id and id to tag



def word_id(file):
    if file:
        id2tag, tag2id, word2id, id2word = {}, {}, {}, {}
        words, tags = set(), set()
        with open(file, mode="r", encoding="utf-8") as fp:
            lines = fp.readlines()
            for line in lines:
                if "/" in line.strip():
                    temp = line.strip().split("/")
                    word = temp[0]
                    tag = temp[1]
                    words.add(word)
                    tags.add(tag)

        for id, word in enumerate(words):
            word2id.update({word: str(id)})
            id2word.update({str(id): word})
        for id, tag in enumerate(tags):
            tag2id.update({tag: str(id)})
            id2tag.update({str(id): tag})
        return id2word,word2id, id2tag, tag2id
    #
    return None

if __name__ == '__main__':
    file = "./data/traindata.txt"
    id2word, word2id, id2tag, tag2id = word_id(file)
