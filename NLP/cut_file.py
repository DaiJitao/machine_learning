import jieba_fast as jieba
import re
import json

def clean_text(text):
    text = str(text)
    # 去掉url地址
    text = re.sub('''http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+''', '', text)
    # 去掉@某某某
    text = re.sub(r"\[.{0,5}\]|//|@.{1,8}:{0,1}", "，", text)
    # text = re.sub('''@.+@.+([\n]|[\t])''', '', text)
    # text = re.sub("(、，)|@|//@|～|>{1,}|\(\)", "，", text)
    text = re.sub("[(。，)(！，)(？，)(、，)@(//@)～>\(\)]{1,}", "，", text)
    # 多个问号变为一个问号
    text = re.sub(r"[。？\?]{2,}", "？", text)
    text = re.sub(r"[！!]{2,}", "！", text)
    # 去掉#某某某# 和单个字母单个数字
    text = re.sub("转发微博|#.{1,20}#|展开全文|([a-zA-Z]|[0-9])", "，", text)
    # ？? -> ?
    text = re.sub(r"(\?？)|(？\?)", "？", text)
    text = re.sub(r"—{2,}|-{2,}", "—", text)
    text = re.sub(r"…{1,}|\.{4,}", "…", text)
    r = u'[/【】●■�→．・🇨🇳９８７６５４３２１０／％［］×\[\]^_`{|}~(:з」∠)]'
    text = re.sub(r, "，", text)
    # 去掉非中文
    not_chinese = r'[^\u4e00-\u9fa5，{}【】（）。：；“‘”…《》、！？——]'
    text = re.sub(not_chinese, " ", text)
    # 多个空格变为1个
    text = re.sub(r"\s{1,}", " ", text)
    text = re.sub(r"[(\s，)(\s,),，(（）)(：，)(： ：)(—，)]{1,}", "，", text).strip()
    return text

if __name__ == '__main__':

    userwords = [line.rstrip() for line in open('./data/userdict.txt', encoding='utf-8')]
    for word in userwords:
        jieba.add_word(word.strip())
    stopwords = [line.rstrip() for line in open('./data/stopwords.txt', encoding='utf-8')]
    # with open("./data/stopwords1.txt", mode="w+", encoding="utf-8") as fp:
    #     s = set(stopwords)
    #     fp.write("\n".join(s))

    file = "./data/hotdata.txt"
    with open(file, mode="r", encoding="utf-8") as fp:
        i = 0
        for line in fp.readlines()[43:]:
            # if i == 8: break

            d = json.loads(line)['content']
            print(i )
            print(d)
            cleanText = clean_text(d)
            print("-"*60 + "清洗之后：")
            print(cleanText)
            c = [word for word in jieba.cut(cleanText)]
            print()
            print(" ".join(c))
            # print("removed Stopwprds:")
            lst = [word for word in c if word not in stopwords]
            print(" ".join(lst))
            print("===============================\n\n")
            i += 1

    text = "📍苏州拙政园  苏州园林的代表作。厅榭精美，山水萦绕，具有浓郁的江南水乡特色。  #遇见美好##带着微博去旅游##行摄江苏##寻找江苏最美风景# "
    # text = re.sub(r"(#.{1,20}#)", " ", text)
    # print(text)
    text = re.sub("转发微博|#.{1,20}#|展开全文|([a-zA-Z]|[0-9])", "", text)

    print(text)
