from pyltp import SentenceSplitter
import os
from pyltp import Segmentor
import jieba
import re,time
from urllib import parse


from LAC import LAC

lac = LAC(mode='seg')

def lac_cut(line):
    # 单个样本输入，输入为Unicode编码的字符串
    text = u"LAC是个优秀的分词工具"
    seg_result = lac.run(line)
    return "|".join(seg_result)

def jieba_cut(line):
    return "|".join(jieba.cut(line))


sents = SentenceSplitter.split('元芳你怎么看？我就趴窗口上看呗！')  # 分句
c = "\n".join(sents)


ltp_data_dir = r'F:\pycharm_workspace\mygithub\machine_learning\NLP\tokenizer\data\ltp_data_v3.4.0'
cws_model_path = os.path.join(ltp_data_dir, 'cws.model')  # 分词模型路径，模型名称为`cws.model`

segmentor = Segmentor()
segmentor.load(cws_model_path)

stop_words_file = r"F:\pycharm_workspace\mygithub\machine_learning\NLP\tokenizer\data\stopwords.txt"
stopWords = [word.strip() for word in open(stop_words_file, mode='r', encoding='utf-8').readlines()]

def ltp_cut(line):
    words = segmentor.segment(line)  # 分词
    return [word for word in words]

print(ltp_cut("你好"))


def title_count(in_file, out_file):
    res_dict = {}
    with open(in_file, mode='r', encoding='utf-8') as fp:
        lines = fp.readlines()
        i = 1
        size = len(lines)
        for line in lines:
            i += 1
            if i % 100000 == 0:
                print("{}% processed".format(i / size * 100))
            # if (i / size) * 100 >= 10:
            #     print("断开行{}".format(i))
            #     break

            line = line.strip()
            if len(line) == 0 or 'NULL' in line:
                continue
            words = ltp_cut(line)
            if len(words) > 0:
                for word in words:
                    key = str(word).strip()
                    if key not in res_dict:
                        res_dict.update({key:1})
                    else:
                        res_dict[key] = res_dict[key] + 1

    # 降序
    sorted_word_num = sorted(res_dict.items(), key=lambda item: int(item[1]), reverse=True)
    print("res_dict={}, sorted_word_num={}".format(len(res_dict), len(sorted_word_num)))
    i = 0
    out = open(out_file, encoding='utf-8', mode='w+')
    for key, value in sorted_word_num:
        i +=1
        if key not in stopWords:
            out.write("{} {}\n".format(key, value))
        if i % 500 == 0:
            out.flush()
            print("写入{}".format(out_file))
    out.close()
    print("写入完成！")




if __name__ == '__main__':
    tb_richmedia_pool = "topic_aa"
    infile = r"F:/pycharm_workspace/mygithub/machine_learning/NLP/tokenizer/data/train/" + tb_richmedia_pool
    outfile = r"F:/pycharm_workspace/mygithub/machine_learning/NLP/tokenizer/data/out/out_" + tb_richmedia_pool
    print("{} , {}".format(infile, outfile))
    title_count(in_file=infile, out_file=outfile)
    segmentor.release()  # 释放模型
