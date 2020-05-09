import json
import configparser
from logger import Logger
from mysql import MySQL
import traceback
import urllib.parse as parse
import sys
import os
import schedule
from threading import Thread
import time
import os

logger = Logger("./logs/user_monitor.log").logger

cf = configparser.ConfigParser()
try:
    cf.read("./config.ini")
    types = cf.sections()
    logger.info("获取配置成功！{}".format(types))
except Exception as e:
    logger.error("获取配置文件{}失败!".format("./config.ini"))
    traceback.print_exc()
    logger.error(e)
    logger.exception("{}".format(e))
    sys.exit(1)

sql_host = cf.get(types[0], 'host')
sql_user = cf.get(types[0], 'user')
sql_password = cf.get(types[0], 'password')
sql_db = cf.get(types[0], 'db')
sql_port = cf.get(types[0], 'port')
douyin_detail_tb = cf.get(types[0], 'douyin_detail_tb')
toutiao_detail_tb = cf.get(types[0], 'toutiao_detail_tb')
toutiao_user_file = cf.get('monitorFile', 'toutiao_user_file')
douyin_user_file = cf.get('monitorFile', 'douyin_user_file')


'''
单用户统计
'''


def list_dir(dir):
    result = []
    if os.path.exists(dir):
        result = os.listdir(dir)  # 列出所有文件
        return result
    else:
        logger.error(dir + "文件夹不存在")
        return result


'''
已作废
'''


def list_dir_1(dir, file):
    result = []
    if os.path.exists(dir):
        files = os.listdir(dir)  # 列出所有文件
        # 判断文件是否存在 否则创建
        if not os.path.isfile(file):
            fd = open(file, "w", encoding='utf-8')
            fd.close()
        with open(file, mode='r+', encoding='utf-8') as fp:
            lines = fp.read().split("\n")[:-1]
            for file in files:
                if file not in lines:
                    fp.write(file)
                    fp.write("\n")
                    result.append(file)
        return result
    else:
        logger.error(dir + "文件夹不存在")


def count_user_id(base_dir, files, character):
    """
    统计文件中用户个数
    :param base_dir:
    :param files:
    :param character:
    :return:
    """
    count = 0
    times = 1
    try:
        for file in files:
            temp = base_dir + "/" + file
            if times % 10 == 0:
                logger.info("统计文件{},character=[{}]数量{}".format(temp, character, count))
            with open(temp, mode='r', encoding='utf-8') as fp:
                lines = fp.readlines()
                for line in lines:
                    if line.strip() == character:
                        count += 1
        return count
    except Exception as e:
        logger.error(e)
        traceback.print_exc()
        logger.exception("{}".format(e))
        return 0


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


def system_count(character, indir, outfile):
    try:
        # grep -rn 'AU:' /mnt/data/toutiao_bak/article/video/*
        cmd = "grep -rn '" + character + "' {}/* > {}".format(indir, outfile)
        res = os.system(cmd)
        if res == 0:
            logger.info("[{}]执行成功".format(cmd))
        else:
            logger.info("[{}]执行失败".format(cmd))
        return res
    except Exception as e:
        logger.info("[{}]执行失败".format(cmd))
        logger.error(e)
        traceback.print_exc()
        logger.exception("{}".format(e))


def __count_all_users(file):
    total_account_res = {}
    with open(file, mode="r", encoding="utf-8") as fp:
        lines = fp.readlines()
        for line in lines:
            user_id = line.split(":")[-1].strip()
            if user_id in total_account_res:
                v = total_account_res[user_id] + 1
                total_account_res.update({user_id: v})
            else:
                total_account_res.update({user_id: 1})

    return total_account_res


def toutiao_count_user_id(users):
    """
    统计头条
    :param users:
    :return:
    """
    out_account_file = "./data/toutiao_account.txt"
    indir = "/mnt/data/toutiao_bak/account"
    # 执行shell
    system_count("BD:", indir=indir, outfile=out_account_file)
    micro = "/mnt/data/toutiao_bak/article/micro"
    text = "/mnt/data/toutiao_bak/article/text"
    video = "/mnt/data/toutiao_bak/article/video"
    out_micro_file = "./data/toutiao_micro.txt"
    out_text_file = "./data/toutiao_text.txt"
    out_video_file = "./data/toutiao_video.txt"
    character = "AU:"
    system_count(character, text, out_text_file)
    system_count(character, micro, out_micro_file)
    system_count(character, video, out_video_file)
    time.sleep(60)
    total_account_res = __count_all_users(out_account_file)
    total_micro_res = __count_all_users(out_micro_file)
    total_text_res = __count_all_users(out_text_file)
    toal_video_res = __count_all_users(out_video_file)
    count = 1
    for user in users:
        user_id = user['user_id'].strip()
        if user_id != None and user_id != "":
            if user_id in total_account_res:
                account_size = total_account_res[user_id]
            else:
                account_size = 0
            if user_id in total_micro_res:
                micro_size = total_micro_res[user_id]
            else:
                micro_size = 0

            if user_id in total_text_res:
                text_size = total_text_res[user_id]
            else:
                text_size = 0
            if user_id in toal_video_res:
                video_size = toal_video_res[user_id]
            else:
                video_size = 0

            article_size = video_size + text_size + micro_size
            total = account_size + article_size
            count_result = {"total": total, "article_total": article_size, "account_total": account_size}
            if count % 10 == 0:
                logger.info("开始统计第{}/{}个头条账号{}".format(count, len(users), user_id))
                logger.info("头条账号{}统计结果:{}".format(user_id, count_result))
            mysql = MySQL(user=sql_user, pwd=sql_password, host=sql_host, db=sql_db, tb=toutiao_detail_tb)
            mysql.update_data_detail(count_result, user_id)
            count += 1
    logger.info("所有头条账号统计完毕！")


def douyin_count_user_id(users):
    """
    统计抖音
    :param users:
    :return:
    """
    out_account_file = "./data/douyin_account.txt"
    indir = "/mnt/data/douyin_bak/account"
    # 执行shell
    system_count("ID:", indir=indir, outfile=out_account_file)
    article_dir = "/mnt/data/douyin_bak/article"  # 101989005631
    out_article_file = "./data/douyin_article.txt"
    character = "AU:"
    system_count(character, article_dir, out_article_file)
    time.sleep(60)
    total_account_res = __count_all_users(out_account_file)
    total_article_res = __count_all_users(out_article_file)
    count = 1
    for user in users:
        user_id = user['user_id'].strip()
        if user_id != None and user_id != "":
            if user_id in total_account_res:
                account_size = total_account_res[user_id]
            else:
                account_size = 0
            if user_id in total_article_res:
                article_size = total_article_res[user_id]
            else:
                article_size = 0

            total = account_size + article_size
            count_result = {"total": total, "article_total": article_size, "account_total": account_size}
            if count % 10 == 0:
                logger.info("开始统计第{}/{}个抖音账号{}".format(count, len(users), user_id))
                logger.info("抖音账号{}统计结果:{}".format(user_id, count_result))
            mysql = MySQL(user=sql_user, pwd=sql_password, host=sql_host, db=sql_db, tb=douyin_detail_tb)
            mysql.update_data_detail(count_result, user_id)
            count += 1
    logger.info("所有抖音账号统计完毕！\n\n")


def count_user_toutiao():
    logger.info("开始统计头条数据量,账号文件:{}".format(toutiao_user_file))
    users = get_user(toutiao_user_file, "toutiao")
    if users:
        toutiao_count_user_id(users)
    else:
        logger.error("无法获取头条账号")
        sys.exit(1)


def count_user_douyin():
    logger.info("开始统计抖音数据量,抖音账号文件：{}".format(douyin_user_file))
    users = get_user(douyin_user_file, "douyin")
    if users:
        douyin_count_user_id(users)
    else:
        logger.error("无法获取抖音账号")
        sys.exit(1)


def main():
    interval = cf.get("userMonitor", "interval")
    unit = cf.get("userMonitor", "unit")
    interval = int(interval)
    if unit == "minute":
        schedule.every(interval=interval).minutes.do(count_user_douyin)
        schedule.every(interval=interval).minutes.do(count_user_toutiao)
        while True:
            schedule.run_pending()
            time.sleep(1)
    elif unit == "hour":
        schedule.every(interval=interval).minutes.do(count_user_douyin)
        schedule.every(interval=interval).minutes.do(count_user_toutiao)
        while True:
            schedule.run_pending()
            time.sleep(1)

    else:
        logger.error("无法识别配置文件参数{}".format(unit))
        sys.exit(1)



if __name__ == '__main__':
    main()
    # if __name__ == '__main__':
    #     # mysql = MySQL(user=user, pwd=password, host=host, db=db, tb=toutiao_detail_tb)
    #     mysql = MySQL(user=user, pwd=password, host=host, db=db, tb=toutiao_detail_tb)
    #     mysql = MySQL(user=user, pwd=password, host=host, db=db, tb=douyin_detail_tb)
    #     count_result = {"total": 25, "article_total": 6, "account_total": 19}
    #     mysql.update_data_detail(count_result, "999")
