"""统计词频"""


def is_number(s):
    try:
        if "." in s:
            return False
        float(s)
        return True
    except ValueError:
        return False

        # try:
        #     import unicodedata
        #     unicodedata.numeric(s)
        #     return True
        # except (TypeError, ValueError):
        #     pass


def isNumber(c):
    if "-" or "." in c:
        return False
    return c >= '0' and c <= '9'


def title_count_all(in_file):
    res_dict = {}
    with open(in_file, mode='r', encoding='utf-8') as fp:
        lines = fp.readlines()
        i = 1
        size = len(lines)
        for line in lines:
            tmp = line.strip().split()
            word = tmp[0]
            num = int(tmp[-1])
            if word not in res_dict:
                res_dict.update({word: num})
            else:
                res_dict[word] = res_dict[word] + num

    return res_dict
    # 降序
    sorted_word_num = sorted(res_dict.items(), key=lambda item: int(item[1]), reverse=True)
    print("res_dict={}, sorted_word_num={}".format(len(res_dict), len(sorted_word_num)))
    out = open(out_file, encoding='utf-8', mode='w+')
    i = 0
    for key, value in sorted_word_num:
        i += 1
        if key not in stopWords:
            out.write("{} {}\n".format(key, value))
        if i % 100 == 0:
            out.flush()
            print("写入{}".format(out_file))
    out.close()
    print("写入完成！")


if __name__ == '__main__':
    in_file_name_aa = r"F:\pycharm_workspace\mygithub\machine_learning\NLP\tokenizer\data\out\out_car.data"
    in_file_name_ab = r"F:\pycharm_workspace\mygithub\machine_learning\NLP\tokenizer\data\out\out_richmedia_aa"
    in_file_name_ac = r"F:\pycharm_workspace\mygithub\machine_learning\NLP\tokenizer\data\out\out_richmedia_ab"

    topic_aa = r"F:\pycharm_workspace\mygithub\machine_learning\NLP\tokenizer\data\out\out_topic_aa"
    topic_ab = r"F:\pycharm_workspace\mygithub\machine_learning\NLP\tokenizer\data\out\out_topic_ab"
    topic_ac = r"F:\pycharm_workspace\mygithub\machine_learning\NLP\tokenizer\data\out\out_topic_ac"
    topic_ad = r"F:\pycharm_workspace\mygithub\machine_learning\NLP\tokenizer\data\out\out_topic_ad"
    topic_ae = r"F:\pycharm_workspace\mygithub\machine_learning\NLP\tokenizer\data\out\out_topic_ae"

    aa_dict = title_count_all(in_file_name_aa)
    ab_dict = title_count_all(in_file_name_ab)
    ac_dict = title_count_all(in_file_name_ac)

    toipic_aa_dict = title_count_all(topic_aa)
    toipic_ab_dict = title_count_all(topic_ab)
    toipic_ac_dict = title_count_all(topic_ac)
    toipic_ad_dict = title_count_all(topic_ad)
    toipic_ae_dict = title_count_all(topic_ae)

    all_word_num = {}
    for key, value in aa_dict.items():
        if key in all_word_num:
            all_word_num[key] = all_word_num[key] + aa_dict[key]
        else:
            all_word_num[key] = aa_dict[key]

    for key, value in ab_dict.items():
        if key in all_word_num:
            all_word_num[key] = all_word_num[key] + ab_dict[key]
        else:
            all_word_num[key] = ab_dict[key]

    for key, value in ac_dict.items():
        if key in all_word_num:
            all_word_num[key] = all_word_num[key] + ac_dict[key]
        else:
            all_word_num[key] = ac_dict[key]

    for key, value in toipic_aa_dict.items():
        if key in all_word_num:
            all_word_num[key] = all_word_num[key] + toipic_aa_dict[key]
        else:
            all_word_num[key] = toipic_aa_dict[key]

    for key, value in toipic_ab_dict.items():
        if key in all_word_num:
            all_word_num[key] = all_word_num[key] + toipic_ab_dict[key]
        else:
            all_word_num[key] = toipic_ab_dict[key]

    for key, value in toipic_ac_dict.items():
        if key in all_word_num:
            all_word_num[key] = all_word_num[key] + toipic_ac_dict[key]
        else:
            all_word_num[key] = toipic_ac_dict[key]

    for key, value in toipic_ad_dict.items():
        if key in all_word_num:
            all_word_num[key] = all_word_num[key] + toipic_ad_dict[key]
        else:
            all_word_num[key] = toipic_ad_dict[key]

    for key, value in toipic_ae_dict.items():
        if key in all_word_num:
            all_word_num[key] = all_word_num[key] + toipic_ae_dict[key]
        else:
            all_word_num[key] = toipic_ae_dict[key]

    # 降序
    sorted_word_num = sorted(all_word_num.items(), key=lambda item: int(item[1]), reverse=True)
    print()
    out_name = "title_count_result.txt"
    out_file = "./data/out/" + out_name
    out_fp = open(out_file, mode='w+', encoding='utf-8')

    size = len(sorted_word_num)
    print("未排序={}，排序{}".format(len(all_word_num), size))
    stop_words_file = r"F:\pycharm_workspace\mygithub\machine_learning\NLP\tokenizer\data\stopwords.txt"
    stopWords = [word.strip() for word in open(stop_words_file, mode='r', encoding='utf-8').readlines()]
    for key, value in sorted_word_num:
        if key not in stopWords:
            out_fp.write("{} {}\n".format(key, value))

    out_fp.close()
    print("写入完成！")
