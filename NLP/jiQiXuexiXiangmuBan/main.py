import nltk

def load_data(in_file):
    cn = []
    en = []
    with open(in_file, mode='r', encoding='utf-8') as file:
        for line in file.readlines():
            line = line.strip().split("\t")
            # 英文分词
            en.append(["BOS"] + nltk.word_tokenize(line[0]) + ["EOS"])
            cn.append(["BOS"] + [word for word in line[1]] + ["EOS"])

    return cn, en

def main():
    # in_file = get_args()
    # 加载训练集
    in_file_train = r"F:\pycharm_workspce\dai_github\machine_learning\NLP\data\seq2seq\train.txt"
    train_cn, train_en = load_data(in_file_train)
    #加载验证集
    in_file_dev = r""
    dev_cn, dev_en = load_data(in_file_dev)

if __name__ == "__main__":
    main()