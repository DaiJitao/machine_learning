import jieba_fast as jieba
import re
import json


def clean_text(text):
    text = str(text)
    # 去掉url地址
    text = re.sub('''http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+''', '', text)
    # 去掉@某某某  text = re.sub(r"@.{1,12}\s", "，", text)
    text = re.sub(r"//@[^@]{1,20}:\s{0,1}|\[.{1,5}\]|@[^@]{1,}:\s{0,1}|@.{1,10}\s", "，", text)
    text = re.sub(r"@[^a].{1,10}","，", text)
    # text = re.sub(r"\[.{0,5}\]|//@.{1,15}[:\s]{1,2}|@.{1,15}[:\s]{1,2}", "，", text)
    text = re.sub(r"分享来自：.{1,6}\s", "", text)
    text = re.sub(r"(？，){1,3}|(。，){1,3}|(！，){1,6}","。", text)
    # 多个问号变为一个问号
    text = re.sub(r"[！!。？\?]{2,}", "！", text)
    # 去掉#某某某# 和单个字母单个数字
    text = re.sub(r"动态|转发|微博|微博转|转发微博|#[^#]{1,10}#|展开全文|([a-zA-Z]|[0-9])", "，", text)
    # ？? -> ?
    text = re.sub(r"(\?？)|(？\?)", "？", text)
    text = re.sub(r"—{2,}|-{2,}", "—", text)
    text = re.sub(r"…{1,}|\.{4,}", "…", text)
    r = u'[/【】●■�→．・🇨🇳９８７６５４３２１０／％［］×\[\]^_`{|}~(:з」∠)]'
    text = re.sub(r, "，", text)
    # 去掉非中文
    not_chinese = r'[^\u4e00-\u9fa5，{}【】（）。：；“‘”…《》、！？——]'
    text = re.sub(not_chinese, " ", text)
    text = re.sub(u".[岁个年只]的", "。", text)
    # 多个空格变为1个
    text = re.sub(r"[，！。、‘’；：\s]{2,6}", "。", text)
    # text = re.sub(r"[(\s，),（）： —]{1,}", "。", text).strip()
    text = re.sub(u"[帅叨哈呵呀哎嘻啊操艹]{1,8}[，。？、！‘’；：·]{0,2}", "。", text)
    text = re.sub(r"^[，！。‘’？、]{1}\b", "", text)
    return text


def clean_cutwords(word):
    if word:
        word = str(word)
        if len(word.strip()) == 2:
            word = re.sub(
                r"[前上下午中今明后][后年日月天午]|位于|第[一二三四五六七八九十]|[期这那上下一二三四五六七八九十多][期秒上下次条张之只朵枝件万千个片首种块套双组段座票根口弯湾头对米位篇叶日月克顿吨排层面包圈天年]",
                "", word)
            return word
        elif len(word.strip()) == 3:
            word = re.sub(r"第[一二三四五六七八九十][期秒次条张之只朵枝件万千个片首种块套双组段座票根口弯湾头对米位篇叶日月克顿吨排层面包圈天年]", "", word)
            return word
        else:
            return word

    return ''


def user_dict(outfile):
    s = set([line.strip() for line in open('./data/userdict.txt', encoding='utf-8')])
    s = [word + " 100 n" for word in s]
    with open(outfile, mode='w', encoding='utf-8') as fp:
        fp.write("\n".join(s))


if __name__ == '__main__1':
    out_file = "./data/userdict1.txt"
    user_dict(out_file)

if __name__ == '__main__':

    jieba.load_userdict('./data/userdict.txt')
    stopwords = [line.rstrip() for line in open('./data/stopwords.txt', encoding='utf-8')]

    file = "./data/hotword.txt"
    with open(file, mode="r", encoding="utf-8") as fp:
        i = 0
        for line in fp.readlines()[:]:
            d = json.loads(line)['content']
            print(i)
            print(d)
            cleanText = clean_text(d)
            print("-" * 60 + "清洗之后：")
            print(cleanText)
            c = [word for word in jieba.cut(cleanText) if len(word.strip()) > 1]
            print()
            print("初始分词：", " ".join(c))
            print("removed Stopwprds:")
            lst1 = [word for word in c if word not in stopwords]
            print("最终分词：", " ".join(lst1))
            print("===============================\n\n")
            i += 1

    text = "正月初四初五"
    print(text)

    # jieba.load_userdict('./data/userdict.txt')
    jieba.load_userdict('./data/supplement.txt')

    text = [w for w in jieba.cut(text)]
    print(text)
