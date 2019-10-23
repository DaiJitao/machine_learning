import json
import re

file = r"F:\pycharm_workspce\dai_github\machine_learning\NLP\data\cleantest.txt"


def load_data(file):
    with open(file, encoding="utf-8", mode='r') as f:
        line = f.readlines()[0]
        data = json.loads(line.strip(), encoding='utf-8')
        return data["content"].strip()


def clean_chinese_text(line):
    '''
    清理中文文本，去除标点符号和数字
    :param line:
    :return:
    '''
    if line:
        line = re.sub(r'\s+', ' ', line)  # trans 多空格 to 空格
        line = re.sub(r'\n', ' ', line)  # trans 换行 to 空格
        line = re.sub(r'\t', ' ', line)  # trans Tab to 空格
        # 去掉干扰信息
        channel_rule = r'车站|列车|车票|火车|自行车|摩托车|列车|作业车|工程车|农用车|清洁车|扫地车|洒水车|垃圾车|环卫车|拖车|拼车|车棚|车库'
        text = re.sub(channel_rule, "", line)
        # 去掉媒体信息
        media = "新华社|新华网|中新社|人民日报"
        rule = r'(%s)[\s\S]{0,30}[0-9]{0,2}月[0-9]{1,2}日电|' % media + \
               r'(%s)[\s\S]{0,30}日电|' % media + \
               r'据(%s)[0-9]{1,2}月[0-9]{1,2}日消息|' % media + \
               r'(%s)[\s\S]{0,30}消息|' % media + \
               r'据(%s)[\s\S]*消息{0,1}|' % media + \
               r'据(%s)[\s\S]*报道|' % media + \
               r'(%s)[\s\S]*摄|' % media + \
               r'(%s)快讯|' % media + \
               r'(%s)电|' % media + \
               r'(%s)发\\|' % media + \
               r'【(%s)】|' % media + \
               r'\[(%s)\]|' % media + \
               r'(%s)讯|' % media + \
               r'来源：(%s)|' % media + \
               r'来源:(%s)|' % media + \
               r'(%s)评论员|' % media + \
               r'\((%s)\)|' % media + \
               r'(%s)记者|' % media + \
               r'（(%s)）' % media
        text = re.sub(rule, "", text)
        # 去掉url地址
        text = re.sub('''http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+''', '', text)
        # 去掉表情:以中括号括起来[开心]
        text = re.sub('''\[([^\[\]]+)\]''', '', text)
        # 去掉@某某某
        text = re.sub('''@.+@.+([\n]|[\t])''', '', text)
        # 去掉#某某某#
        text = re.sub('''#.+#''', '', text)
        # 去掉特殊标点符号
        r = u'[!"#$%&\'()*+,-./:;<=>《￥★▼》，。·“”（）、；：？【】—！●■�0123456789．・９８７６５４３２１０／％［］×…?@[\\]^_`{|}~]'
        cleaned = re.sub(r, '', text)
        return cleaned


if __name__ == "__main__":
    data = (load_data(file))
    text = clean_chinese_text(data)
    print(data)
    print(text)
