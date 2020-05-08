import json
import configparser
from data_monitor import count
from logger import Logger
from mysql import MySQL
import traceback
import urllib.parse as parse
import sys

logger = Logger("./logs/user_monitor.log").logger

logger = Logger("./logs/user_monitor.log").logger
cf = configparser.ConfigParser()
try:
    cf.read("./config.ini")
    types = cf.sections()
    logger.info("获取配置成功！{}".format(types))
except Exception as e:
    traceback.print_exc()
    logger.error(e)
    logger.exception("{}".format(e))
    sys.exit(1)


host = cf.get(types[0], 'host')
user = cf.get(types[0], 'user')
password = cf.get(types[0], 'password')
db = cf.get(types[0], 'db')
port = cf.get(types[0], 'port')
douyin_detail_tb = cf.get(types[0], 'douyin_detail_tb')
toutiao_detail_tb = cf.get(types[0], 'toutiao_detail_tb')
toutiao_user_file=cf.get('monitorFile', 'toutiao_user_file')
douyin_user_file=cf.get('monitorFile', 'douyin_user_file')


'''
单用户统计
'''
def get_user(file, user_type):
    '''
    获取用户信息
    :param file:
    :param user_type:
    :return: [{'url': '', 'name': '', 'first_classification': 1, 'second_classification': 1, 'province': '21', 'city': 0, 'county': 0, 'user_id': '3908764883'}]
    '''
    users = []
    if user_type == "douyin":
        with open(file, mode="r", encoding="utf-8") as fp:
            for line in fp.readlines():
                json_line = json.loads(line.strip(), encoding="utf-8")
                if 'url' in json_line:
                    path = parse.urlparse(json_line['url']).path
                    index = path.rindex("/")
                    user_id = path[index + 1:]
                    json_line['user_id'] = user_id
                users.append(json_line)

    if user_type == "toutiao":
        with open(file, mode="r", encoding="utf-8") as fp:
            for line in fp.readlines():
                json_line = json.loads(line.strip(), encoding="utf-8")
                if 'url' in json_line:
                    path = parse.urlparse(json_line['url']).path
                    start_index = path.index("r/") + 2
                    end_index = path.rindex("/")
                    user_id = path[start_index:end_index]
                    # print(path + " => " + user_id)
                    json_line['user_id'] = user_id
                users.append(json_line)

    return users


def douyin_user_count(user_id):
    character = "ID:{}".format(user_id)
    douyin_dir = "/mnt/data/douyin_bak/account"
    #  grep -o "ID:1300287065" /mnt/data/douyin_bak/account/* |wc -l
    size = count(character, douyin_dir) # 账号信息数据量
    account_size = 0 if size == None else size

    article_dir = "/mnt/data/douyin_bak/article"
    #  grep -o AU:3132868345 /mnt/data/douyin_bak/article/* |wc -l
    character = "AU:{}".format(user_id)
    article_size = count(character, article_dir)
    article_size = 0 if article_size == None else article_size
    total = account_size + article_size
    return total, account_size,article_size

def toutiao_user_count(user_id):
    character = "BD:{}".format(user_id)
    douyin_dir = "/mnt/data/toutiao_bak/account"
    #  grep -o "BD:3908764883" /mnt/data/toutiao_bak/account/* |wc -l
    size = count(character, douyin_dir) # 账号信息数据量
    account_size = 0 if size == None else size

    micro = "/mnt/data/toutiao_bak/article/micro"
    text = "/mnt/data/toutiao_bak/article/text"
    video = "/mnt/data/toutiao_bak/article/video"
    #  grep -o AU:98252811911 /mnt/data/toutiao_bak/article/micro/* |wc -l
    character = "AU:{}".format(user_id)
    micro_size = count(character, micro)
    micro_size = 0 if micro_size == None else micro_size
    text_size = count(character,text)
    text_size = 0 if text_size == None else text_size
    video_size = count(character,video)
    video_size = 0 if video_size == None else video_size
    article_size = micro_size + text_size + video_size
    total = article_size + account_size

    return total, account_size, article_size


def count_user_toutiao():
    users = get_user(toutiao_user_file, "toutiao")
    for user in users:
        user_id = user['user_id']
        if user_id != None and user_id != "":
            total, account_size, article_size = toutiao_user_count(user_id)
            count_result = {"total":total, "article_total": article_size, "account_total": account_size}
            mysql = MySQL(user=user, pwd=password, host=host, db=db, tb=toutiao_detail_tb)
            mysql.update_data_detail(count_result,user_id)

def count_user_douyin():
    users = get_user(douyin_user_file, "douyin")
    for user in users:
        user_id = user['user_id']
        if user_id != None and user_id != "":
            total, account_size, article_size = toutiao_user_count(user_id)
            count_result = {"total":total, "article_total": article_size, "account_total": account_size}
            mysql = MySQL(user=user, pwd=password, host=host, db=db, tb=douyin_detail_tb)
            mysql.update_data_detail(count_result,user_id)

def main():
    count_user_douyin()
    count_user_toutiao()

if __name__ == '__main__':
    main()
