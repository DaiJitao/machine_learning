import subprocess
import time
from logger import Logger
from mysql import MySQL
import schedule
import traceback
from threading import Thread
from multiprocessing import Process  # 多进程
import configparser
import datetime # 内置
import sys

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
charset = cf.get(types[0], 'charset')
toutiao_table = cf.get(types[0], 'toutiao_tb')
douyin_tb = cf.get(types[0], 'douyin_tb')

character = "%&"


class Field():
    def __init__(self):
        pass

    @staticmethod
    def get_fields():
        count_dict = {'total_data': 0, 'cycle_num': 0, 'account_total': 0,
                      'article_total': 0, 'update_total': 0,'comment_total': 0,
                      'article_micro_total': 0,'article_text_total': 0,
                      'article_video_total': 0, 'video_total': 0,
                      'article_cycle_num': 0, 'update_text_total': 0,
                      'article_text_cycle_num': 0,
                      'article_video_cycle_num': 0, 'updata_micro_total': 0,
                      'update_video_total': 0, 'update_video_cycle': 0,
                      'update_cycle_num': 0,  'comment_cycle': 0,
                      'update_micro_cycle': 0,
                       'account_cycle_num': 0, 'cycle_type': '1', 'video_cycle': 0,
                      'article_micro_cycle_num': 0, 'update_text_cycle': 0}
        return count_dict


def count(character, file_dir):
    cmd = 'grep -o "{}"  {}/* | wc -l'.format(character, file_dir)
    logger.info("执行命令[ " + cmd + " ]")
    try:
        call = subprocess.getstatusoutput(cmd)
        if call[0] == 0:
            logger.info(file_dir + "返回值: " + str(call))
            return int(call[1])
        else:
            logger.error(str(call))
    except Exception as e:
        traceback.print_stack()
        logger.error(e)
        logger.exception(e)


def video_count(type, video_dir):
    cmd = 'ls {}/* | grep {} | wc -l'.format(video_dir, type)
    logger.info("执行命令[ " + cmd + " ]")
    try:
        call = subprocess.getstatusoutput(cmd)
        if call[0] == 0:
            logger.info(video_dir + "返回值: " + str(call))
            return int(call[1])
        else:
            logger.error(str(call))
    except Exception as e:
        # traceback.print_stack()
        logger.error(e)
        logger.exception(e)


def douyin_count():
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

    mysql = MySQL(user=user, pwd=password, host=host, db=db, tb=douyin_tb)
    mysql.update_data(count_result)


def toutiao_count():
    # 账号信息
    account_dir = "/mnt/data/toutiao/account"
    account_size = count(character, account_dir)
    account_size = 0 if account_size == None else account_size
    # 文章 微头条
    article_micro_dir = "/mnt/data/toutiao/article/micro"
    article_text_dir = "/mnt/data/toutiao/article/text"
    article_video_dir = "/mnt/data/toutiao/article/video"
    article_micro_size = count(character, article_micro_dir)
    article_text_size = count(character, article_text_dir)
    article_video_size = count(character, article_video_dir)
    article_micro_size = 0 if article_micro_size == None else article_micro_size
    article_text_size = 0 if article_text_size == None else article_text_size
    article_video_size = 0 if article_video_size == None else article_video_size
    article_size = article_text_size + article_micro_size + article_video_size
    # comment
    comment_dir = "/mnt/data/toutiao/comment"
    comment_size = count(character, comment_dir)
    comment_size = 0 if comment_size == None else comment_size
    # update
    update_micro_dir = "/mnt/data/toutiao/update/micro"
    update_text_dir = "/mnt/data/toutiao/update/text"
    update_video_dir = "/mnt/data/toutiao/update/video"
    update_micro_size = count(character, update_micro_dir)
    update_text_size = count(character, update_text_dir)
    update_video_size = count(character, update_video_dir)
    update_micro_size = 0 if update_micro_size == None else update_micro_size
    update_text_size = 0 if update_text_size == None else update_text_size
    update_video_size = 0 if update_video_size == None else update_video_size
    update_size = update_text_size + update_micro_size + update_video_size
    # video
    # video_dir = "/mnt/data/toutiao/video"
    # video_size = video_count("mp4", video_dir)
    # video_size = 0 if video_dir == None else video_size
    total_data = account_size + article_size + update_size + comment_size
    count_result = Field.get_fields()
    count_result['total_data'] = total_data
    count_result['account_total'] = account_size
    count_result['article_total'] = article_size
    count_result['update_total'] = update_size
    count_result['comment_total'] = comment_size
    count_result['article_micro_total'] = article_micro_size
    count_result['article_text_total'] = article_text_size
    count_result['article_video_total'] = article_video_size
    count_result['updata_micro_total'] = update_micro_size
    count_result['update_text_total'] = update_text_size
    count_result['update_video_total'] = update_video_size

    mysql = MySQL(user=user, pwd=password, host=host, db=db, tb=toutiao_table)
    mysql.update_data(count_result)


def toutiao_task():
    t = Thread(target=toutiao_count)
    t.start()


def douyin_task():
    t = Thread(target=douyin_count)
    t.start()


def main():
    interval = int(cf.get(types[1], "interval"))
    if "second" == cf.get(types[1], 'unit'):
        schedule.every(interval).seconds.do(toutiao_task)
        schedule.every(interval).seconds.do(douyin_task)
        while True:
            schedule.run_pending()
            # time.sleep(10)
    elif "hour" == cf.get(types[1], 'unit'):
        schedule.every(interval).hours.do(toutiao_task)
        schedule.every(interval).hours.do(douyin_task)
        while True:
            schedule.run_pending()
    elif "minute" == cf.get(types[1], 'unit'):
        schedule.every(interval).minutes.do(toutiao_task)
        schedule.every(interval).minutes.do(douyin_task)
        while True:
            schedule.run_pending()


if __name__ == '__main__':
    main()
