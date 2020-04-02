import json
import configparser
from monitor.logger import Logger
import traceback
import sys
import urllib.parse as parse

logger = Logger("./logs/all_monitor.log").logger
cf = configparser.ConfigParser()
try:
    cf.read("./config.ini")
    types = cf.sections()
    monitorFile = types[3]
    logger.info("获取配置成功！{}".format(types))
except Exception as e:
    logger.error("获取配置失败！")
    traceback.print_exc()
    logger.error(e)
    logger.exception("{}".format(e))
    sys.exit(1)

toutiao_user_file = cf.get(monitorFile, "toutiao_user_file")
douyin_user_file = cf.get(monitorFile, "douyin_user_file")


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


if __name__ == '__main__':
    users = get_user(toutiao_user_file, "toutiao")
    print(users)
