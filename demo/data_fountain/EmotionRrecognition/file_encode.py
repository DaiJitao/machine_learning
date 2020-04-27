import os
import sys
import codecs
import chardet


def detect_encoding(file):
    with open(file, "rb") as f_in:
        data = f_in.readlines()[0]
        code_type = chardet.detect(data)['encoding']

    return code_type



def convert_decode(file_name, out_file, encode="GBK", out_code="UTF-8"):
    """
    该程序用于将目录下的文件从指定格式转换到指定格式，默认的是GBK转到UTF-8
    :param file:    文件路径
    :param in_code:  输入文件格式
    :param out_code: 输出文件格式
    :return:
    """
    out_path = '输出文件路径'
    try:
        with codecs.open(file_name, 'r', encode) as f_in:
            new_content = f_in.read()
            f_out = codecs.open(out_file, 'w', out_code)
            f_out.write(new_content)
            f_out.close
    except IOError as err:
        print("I/O error: {0}".format(err))

if __name__ == '__main__':
    base_dir = r"F:\NLP\报名比赛\疫情期间网民情绪识别\train_ dataset"
    file_train_csv = base_dir + r"\nCoV_100k_train.labled.csv"
    print(detect_encoding(file=file_train_csv))
    outfile = base_dir + r"\utf8_nCoV_100k_train.labled.csv"
    convert_decode(file_train_csv, outfile, encode="GB2312")