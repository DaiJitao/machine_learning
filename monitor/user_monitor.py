import json
import configparser
from monitor.logger import Logger
from monitor.data_monitor import toutiao_user_file, douyin_user_file, count
from monitor.mysql import MySQL
import traceback
import urllib.parse as parse
import sys

logger = Logger("./logs/all_monitor.log").logger

logger = Logger("./logs/all_monitor.log").logger
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
user_toutiao_tb = cf.get(types[0], 'user_toutiao_tb')
user_douyin_tb = cf.get(types[0], 'user_douyin_tb')

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


def update_mysql_user():
    """
    更新数据库
    :return:
    """

    mysql = MySQL(user=user, pwd=password, host=host, db=db, tb=user_douyin_tb)


def douyin_user_count(user_id):
    character = "ID:{}".format(user_id)
    douyin_dir = "/mnt/data/douyin_bak/account"
    douyin_size = count(character, douyin_dir) # 账号信息数据量
    account_size = 0 if douyin_size == None else douyin_size
    article_dir = "/mnt/data/toutiao/article"
    character = "AU:{}".format(user_id)
    article_size = count(character, article_dir)
    article_size = 0 if article_size == None else article_size



    micro_size = 0 if micro_size == None else micro_size
    update_dir = "/mnt/data/douyin/update"
    update_size = count(character, update_dir)
    update_size = 0 if update_size == 0 else update_size
    video_dir = "/mnt/data/douyin/video"
    video_size = video_count("mp4", video_dir)
    video_size = 0 if video_dir == None else video_size
    # 总量数据
    total_data = account_size + article_size + update_size + video_size
    count_result = Field.get_fields()
    count_result['total_data'] = total_data
    count_result['account_total'] = account_size
    count_result['article_total'] = article_size
    count_result['update_total'] = update_size
    count_result['video_total'] = video_size
    count_result['cycle_type'] = interval

    mysql = MySQL(user=user, pwd=password, host=host, db=db, tb=douyin_tb)
    mysql.update_data(count_result)


if __name__ == '__main__':
    users = get_user(douyin_user_file, "douyin")
    for user in users:
        id = user['user_id']
        print(id)
        # print(user)
