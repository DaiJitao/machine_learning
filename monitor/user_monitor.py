import json
import configparser
from monitor.logger import Logger
from monitor.data_monitor import toutiao_user_file, douyin_user_file, count

import urllib.parse as parse

logger = Logger("./logs/all_monitor.log").logger

def get_user(file, user_type):
    users = []
    if user_type == "douyin":
        with open(file, mode="r", encoding="utf-8") as fp:
            for line in fp.readlines():
                json_line = json.loads(line.strip(), encoding="utf-8")
                if 'url' in json_line.keys():
                    path = parse.urlparse(json_line['url']).path
                    index = path.rindex("/")
                    user_id = path[index + 1:]
                    users.append(user_id)

    if user_type == "toutiao":
        with open(file, mode="r", encoding="utf-8") as fp:
            for line in fp.readlines():
                json_line = json.loads(line.strip(), encoding="utf-8")
                if 'url' in json_line.keys():
                    path = parse.urlparse(json_line['url']).path
                    start_index = path.index("r/")+2
                    end_index = path.rindex("/")
                    user_id = path[start_index:end_index]
                    print(path + " => " + user_id)
                    users.append(user_id)

    return users


def douyin_user_count(user_id):
    character = "ID:{}".format(user_id)
    douyin_dir = "/mnt/data/douyin/account"
    douyin_size = count(character, douyin_dir)
    account_size = 0 if douyin_size == None else douyin_size
    article_dir = "/mnt/data/douyin/article"
    article_size = count(character, article_dir)
    article_size = 0 if article_size == None else article_size
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
    users = get_user(toutiao_user_file, "toutiao")
    print(users)