import configparser
from logger import Logger
import traceback
import sys
from query_sql import get_sql
import pymysql
import datetime

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


class MySQL():
    def __init__(self, host, user, pwd, db, tb, port=3306, charset="utf8"):
        self.host = host
        self.user = user
        self.password = pwd
        self.db = db
        self.port = port
        self.tb = tb
        self.charset = charset
        self.connection = pymysql.connect(host=host, user=user, password=pwd, db=db, port=port, charset=charset)

    def update_data(self, count_result):
        """更新一条数据"""
        try:
            with self.connection.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
                sql = 'SELECT * FROM ' + self.tb + ' ORDER BY time_update DESC LIMIT 1;'
                count = cursor.execute(sql)
                sql_result = cursor.fetchone()
                logger.info("{0} data size: {1} ,data:{2}".format(self.tb, count, sql_result))
                sql = gen_sql(self.tb, count_result=count_result, sql_result=sql_result)
                # 执行sql语句
                logger.info("Executing sql on {} table\n {}\n".format(self.tb, sql))
                cursor.execute(sql)
                self.connection.commit()
                logger.warn("successfully executed and commited the aboved sql on {}! ".format(self.tb))
        except Exception as e:
            logger.error(e)
            logger.exception("{}".format(e))
            self.connection.rollback()
            logger.error("update " + self.tb + " error! mysql rollbacked!")
        finally:
            self.connection.close()

    def update_data_detail(self, count_result, user_id):
        """具体账号：更新一条数据"""
        try:
            with self.connection.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
                sql_t = "SELECT * FROM " + self.tb + " WHERE user_id='" + user_id + "' ORDER BY time_update DESC LIMIT 1;"
                print("执行SQL: {}".format(sql_t))
                count = cursor.execute(sql_t)
                sql_result = cursor.fetchone()
                logger.info("{0} data size: {1} ,data:{2}".format(self.tb, count, sql_result))
                sql = gen_sql_detail(self.tb, count_result=count_result, sql_result=sql_result, user_id=user_id)
                # 执行sql语句
                logger.info("Executing sql on {} table\n {}\n".format(self.tb, sql))
                cursor.execute(sql)
                self.connection.commit()
                logger.warn("successfully executed and commited the aboved sql on {}! ".format(self.tb))
        except Exception as e:
            logger.error(e)
            logger.exception("{}".format(e))
            self.connection.rollback()
            logger.error("update " + self.tb + " error! mysql rollbacked!")
        finally:
            self.connection.close()

    def last_week_data(self):
        """获取上周最新的一条数据"""
        try:
            sql_mod = get_sql()
            with self.connection.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
                sql = sql_mod.replace("##table##", self.tb)
                count = cursor.execute(sql)
                sql_result = cursor.fetchone()
                logger.info("上周数据 size: {} ,data:{}".format(count, sql_result))
                return sql_result
        except Exception as e:
            logger.error(e)
            logger.exception("{}".format(e))
            self.connection.rollback()
            logger.error("update " + self.tb + " error! mysql rollbacked!")
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

    def latest_data(self):
        """获取最新的一条数据
        :return dict type
        """
        try:
            with self.connection.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
                sql = 'SELECT * FROM ' + self.tb + ' ORDER BY time_update DESC LIMIT 1;'
                count = cursor.execute(sql)
                sql_result = cursor.fetchone()
                logger.info("data size: {} ,data:{}".format(count, sql_result))
                return sql_result
        except Exception as e:
            logger.error(e)
            logger.exception("{}".format(e))
            self.connection.rollback()
            logger.error("update " + self.tb + " error! mysql rollbacked!")
        finally:
            self.connection.close()


def gen_sql(tb, count_result, sql_result):
    '''

    :param count_result: 统计结果
    :param sql_result: SQL数据库中的结果
    :return: 组装的SQL语句
    '''
    sql = 'INSERT INTO ' + tb + ' (' \
                                'total_data, cycle_type, cycle_num,' \
                                'account_total, account_cycle_num,' \
                                'article_total, article_cycle_num,' \
                                'article_text_total, article_text_cycle_num,' \
                                'article_micro_total,article_micro_cycle_num,' \
                                'article_video_total, article_video_cycle_num,' \
                                'update_total, update_cycle_num,' \
                                'updata_micro_total,update_micro_cycle,' \
                                'update_text_total,update_text_cycle,' \
                                'update_video_total, update_video_cycle,' \
                                'comment_total, comment_cycle,' \
                                'video_total,video_cycle' \
                                ') VALUES ({0}, {1}, {2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13}, {14},{15},{16},{17},{18},{19},{20},{21},{22}, {23},{24});'
    cycle_type = count_result['cycle_type']  # 周期量的类型
    # 计算数据总量
    total_data = sql_result['total_data']
    if count_result['total_data'] > total_data:
        cycle_num = count_result['total_data'] - total_data  # 周期量
        total_data = count_result['total_data']
    else:
        cycle_num = 0
    # 用户总量
    account_total = sql_result['account_total']
    if count_result['account_total'] > account_total:
        account_cycle_num = count_result['account_total'] - account_total
        account_total = count_result['account_total']
    else:
        account_cycle_num = 0
    # 文章
    article_total = sql_result['article_total']
    if count_result['article_total'] > article_total:
        article_cycle_num = count_result['article_total'] - article_total
        article_total = count_result['article_total']
    else:
        article_cycle_num = 0
    # text
    article_text_total = sql_result['article_text_total']
    if count_result['article_text_total'] > article_text_total:
        article_text_cycle_num = count_result['article_text_total'] - article_text_total
        article_text_total = count_result['article_text_total']
    else:
        article_text_cycle_num = 0

    article_micro_total = sql_result['article_micro_total']
    if count_result['article_micro_total'] > article_micro_total:
        article_micro_cycle_num = count_result['article_micro_total'] - article_micro_total
        article_micro_total = count_result['article_micro_total']
    else:
        article_micro_cycle_num = 0

    article_video_total = sql_result['article_video_total']
    if count_result['article_video_total'] > article_video_total:
        article_video_cycle_num = count_result['article_video_total'] - article_video_total
        article_video_total = count_result['article_video_total']
    else:
        article_video_cycle_num = 0

    update_total = sql_result['update_total']
    if count_result['update_total'] > update_total:
        update_cycle_num = count_result['update_total'] - update_total
        update_total = count_result['update_total']
    else:
        update_cycle_num = 0

    updata_micro_total = sql_result['updata_micro_total']
    if count_result['update_micro_cycle'] > updata_micro_total:
        update_micro_cycle = count_result['update_micro_cycle'] - updata_micro_total
        updata_micro_total = count_result['updata_micro_total']
    else:
        update_micro_cycle = 0

    update_text_total = sql_result['update_text_total']
    if count_result['update_text_total'] > update_text_total:
        update_text_cycle = count_result['update_text_total'] - update_text_total
        update_text_total = count_result['update_text_total']
    else:
        update_text_cycle = 0

    update_video_total = sql_result['update_video_total']
    if count_result['update_video_total'] > update_video_total:
        update_video_cycle = count_result['update_video_total'] - update_video_total
        update_video_total = count_result['update_video_total']
    else:
        update_video_cycle = 0

    comment_total = sql_result['comment_total']
    if comment_total < count_result['comment_total']:
        comment_cycle = count_result['comment_total'] - comment_total
        comment_total = count_result['comment_total']
    else:
        comment_cycle = 0

    video_total = sql_result['video_total']
    if count_result['video_total'] > video_total:
        video_cycle = count_result['video_total'] - video_total
        video_total = count_result['video_total']
    else:
        video_cycle = 0

    new_sql = sql.format(total_data, cycle_type, cycle_num,
                         account_total, account_cycle_num,
                         article_total, article_cycle_num,
                         article_text_total, article_text_cycle_num,
                         article_micro_total, article_micro_cycle_num,
                         article_video_total, article_video_cycle_num,
                         update_total, update_cycle_num,
                         updata_micro_total, update_micro_cycle,
                         update_text_total, update_text_cycle,
                         update_video_total, update_video_cycle,
                         comment_total, comment_cycle,
                         video_total, video_cycle
                         )
    return new_sql


def gen_sql_detail(tb, count_result, sql_result, user_id):
    '''

    :param count_result: 统计结果
    :param sql_result: SQL数据库中的结果
    :return: 组装的SQL语句
    '''
    user_id = "'" + user_id + "'"
    if sql_result:
        total = sql_result['total']
        if total < count_result['total']:
            total_cycle = count_result['total'] - total
            total = count_result['total']
        else:
            total_cycle = 0

        article_total = sql_result['article_total']
        if article_total < count_result['article_total']:
            article_cycle = count_result['article_total'] - article_total
            article_total = count_result['article_total']
        else:
            article_cycle = 0
        account_total = sql_result['account_total']
        if account_total < count_result['account_total']:
            account_cycle = count_result['account_total'] - account_total
            account_total = count_result['account_total']
        else:
            account_cycle = 0

        sql = "INSERT INTO " + tb + \
              " (user_id, total, total_cycle, article_total, article_cycle, account_total, account_cycle) VALUES ({0},{1}, {2},{3},{4},{5},{6});". \
                  format(user_id, total, total_cycle, article_total, article_cycle, account_total, account_cycle)
        return sql
    else: # sql_result =None
        total = count_result['total']
        total_cycle = 0
        article_total = count_result['article_total']
        article_cycle = 0
        account_total = count_result['account_total']
        account_cycle = 0
        sql = "INSERT INTO " + tb + \
              " (user_id, total, total_cycle, article_total, article_cycle, account_total, account_cycle) VALUES ({0},{1}, {2},{3},{4},{5},{6});". \
                  format(user_id, total, total_cycle, article_total, article_cycle, account_total, account_cycle)
        return sql


# if __name__ == '__main__':
#     pass
# mysql = MySQL(user=user, pwd=password, host=host, db=db, tb=douyin_tb)
# sql_result = mysql.latest_data()
# mysql = MySQL(user=user, pwd=password, host=host, db=db, tb=douyin_tb)
# mysql.update_data(sql_result)
