import configparser
from monitor.logger import Logger
import pymysql
import datetime

logger = Logger("./logs/all_monitor.log").logger

cf = configparser.ConfigParser()
cf.read("./config.ini")
types = cf.sections()
logger.info("获取配置成功！{}".format(types))

host = cf.get(types[0], 'host')
user = cf.get(types[0], 'user')
password = cf.get(types[0], 'password')
db = cf.get(types[0], 'db')
port = cf.get(types[0], 'port')
charset = cf.get(types[0], 'charset')

fields = 'total_data, cycle_type, cycle_num,account_total,account_cycle_num,article_total,article_cycle_num,' \
         'article_text_total,article_text_cycle_num'


class MySQL():
    def __init__(self, host, user, pwd, db, port=3306, charset="utf8"):
        self.host = host
        self.user = user
        self.password = pwd
        self.db = db
        self.port = port
        self.charset = charset
        self.connection = pymysql.connect(host=host, user=user, password=pwd, db=db, port=port, charset=charset)

    def print_data(self):
        try:
            with self.connection.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
                sql = 'SELECT * FROM toutiao_tb ORDER BY time_update DESC LIMIT 1;'
                count = cursor.execute(sql)
                print("总数量： " + str(count))
                temp = cursor.fetchone()
                print("temp: ", temp)
                print("", type(temp))
        except Exception as e:
            logger.error(e)
            logger.exception("{}".format(e))
        finally:
            self.connection.close()


    def print_data(self):
        try:
            with self.connection.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
                sql = 'SELECT * FROM toutiao_tb ORDER BY time_update DESC LIMIT 1;'
                count = cursor.execute(sql)
                logger.info("总数量： " + str(count))
                temp = cursor.fetchone()
                print("temp: ", temp)
                print("", type(temp))
        except Exception as e:
            logger.error(e)
            logger.exception("{}".format(e))
        finally:
            self.connection.close()


if __name__ == '__main__':
    mysql = MySQL(user=user, pwd=password, host=host, db=db)
    mysql.print_data()
