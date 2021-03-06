import smtplib
from email.mime.text import MIMEText
from email.header import Header
import traceback
import sys
from mysql import MySQL
import datetime
from threading import Thread
from logger import Logger
from mysql import MySQL
import schedule
import configparser

logger = Logger("./logs/all_monitor.log").logger
cf = configparser.ConfigParser()
try:
    cf.read("./config.ini")
    types = cf.sections()
    logger.info("获取配置成功！{}".format(types))
except Exception as e:
    logger.error("获取配置失败！")
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

email = types[2]
interval = cf.get(email, 'interval')
smtp_server = cf.get(email, 'smtp_server')


def send_email(smtp_server, receivers, email_content, from_addr='976185561@qq.com'):
    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    message = MIMEText(email_content, 'plain', 'utf-8')
    message['From'] = Header("基础技术研发部", 'utf-8')  # 发送者
    message['To'] = Header(",".join(receivers), 'utf-8')  # 接收者

    subject = '自媒体采集系统数据采集情况报告'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        # 开启发信服务，这里使用的是加密传输
        server = smtplib.SMTP_SSL()
        server.connect(smtp_server, 465)
        # 登录发信邮箱
        password = 'lrejsniijyjrbcgd'
        server.login(from_addr, password)

        server.sendmail(from_addr, receivers, message.as_string())
        logger.info("邮件发送成功-->{}".format(receivers))
    except smtplib.SMTPException:
        logger.error("无法发送邮件")
        logger.exception("".format(e))

    finally:
        server.quit()


def gen_content(latest_sql_result, lweek_sql_result, type_name):
    '''
        组合邮件内容
    :param latest_sql_result: 最新一条数据
    :param lweek_sql_result: 上周最新一条数据
    :param type:
    :return:
    '''
    if type_name == "toutiao":
        type = "头条号"
    elif type_name == "douyin":
        type = "抖音号"
    result = []
    cycle_type = latest_sql_result['cycle_type']  # 周期量的类型
    # strftime('%Y-%m-%d %H:%M:%S')
    time_insert = latest_sql_result['time_insert']  # 结束时间
    # time_start = time_insert - datetime.timedelta(minutes=int(cycle_type))
    if type_name == "toutiao":
        time_scope = "报告时间:\t" + time_insert.strftime('%Y{0}%m{1}%d %H:%M').format('/', '/')
        result.append(time_scope)
        result.append("-" * 76)

    # cycle_type = "周期的类型:每隔" + cycle_type + "分钟"
    # result.append(cycle_type)
    # 计算数据总量
    total_data = latest_sql_result['total_data']
    week_data = lweek_sql_result['total_data']
    plus = total_data - week_data
    total_data_str = type + "数据采集量\t" + str(total_data) + "\t条,本周增量\t" + str(plus) + "\t条"
    result.append(total_data_str)

    account_total = latest_sql_result['account_total']
    week_data = lweek_sql_result['account_total']
    plus = account_total - week_data
    account_srt = type + "账号信息采集量\t" + str(account_total) + "\t条,本周增量\t" + str(plus) + "\t条"
    result.append(account_srt)

    # 文章
    if type_name == "toutiao":
        article_total = latest_sql_result['article_total']
        week_data = lweek_sql_result['article_total']
        plus = article_total - week_data
        result.append(type + "文章采集量" + str(article_total) + "\t条,本周增量\t" + str(plus) + "\t条")

    # micro
    if type_name == "toutiao":
        article_micro_total = latest_sql_result['article_micro_total']
        week_data = lweek_sql_result['article_micro_total']
        plus = article_micro_total - week_data
        result.append(type + "微头条采集量" + str(article_micro_total) + "\t条,本周增量\t" + str(plus) + "\t条")

    # update_total = latest_sql_result['update_total']
    # week_data = lweek_sql_result['update_total']
    # plus = update_total - week_data
    # result.append(type + "更新信息量" + str(update_total) + "\t条,本周增量\t" + str(plus) + "\t条")

    if type_name == "toutiao":
        comment_total = latest_sql_result['comment_total']
        week_data = lweek_sql_result['comment_total']
        plus = comment_total - week_data
        result.append(type + "评论数据总量" + str(comment_total) + "\t条,本周增量\t" + str(plus) + "\t条")

    if type_name == "douyin":
        video_total = latest_sql_result['video_total']
        week_data = lweek_sql_result['video_total']
        plus = video_total - week_data
        result.append(type + "视频采集量:" + str(video_total) + "\t条,本周增量\t" + str(plus) + "\t条")

    result = "\n".join(result)
    return result


def send_email_all():
    receivers = cf.get(email, 'receivers')  # 动态获取邮件接受者
    receivers = receivers.split(",")
    logger.info("receivers:{}".format(receivers))
    try:
        latest_mysql = MySQL(user=user, pwd=password, host=host, db=db, tb=toutiao_table)
        latest_sql_result = latest_mysql.latest_data()  # 最新的一天数据
        mysql = MySQL(user=user, pwd=password, host=host, db=db, tb=toutiao_table)
        lweek_res = mysql.last_week_data()
        result_toutiao = gen_content(latest_sql_result, lweek_res, "toutiao")
        mysql = MySQL(user=user, pwd=password, host=host, db=db, tb=douyin_tb)
        latest_sql_result = mysql.latest_data()
        mysql = MySQL(user=user, pwd=password, host=host, db=db, tb=douyin_tb)
        lweek_res = mysql.last_week_data()
        result_douyin = gen_content(latest_sql_result, lweek_res, "douyin")
        t = "\n" + "-" * 76 + "\n"
        result = "自媒体采集系统采集情况报告：" + t  \
                 + result_toutiao + t + result_douyin + t
        send_email(smtp_server, receivers=receivers, email_content=result)

    except Exception as e:
        traceback.print_exc()
        logger.error(e)
        logger.exception("{}".format(e))


def send_email_task():
    t = Thread(target=send_email_all)
    t.start()


def main1():
    time = int(interval)
    if "second" == cf.get(email, 'unit'):
        schedule.every(time).seconds.do(send_email_task)
        while True:
            schedule.run_pending()
    elif "hour" == cf.get(email, 'unit'):
        schedule.every(time).hours.do(send_email_task)
        while True:
            schedule.run_pending()
    elif "minute" == cf.get(email, 'unit'):
        schedule.every(time).minutes.do(send_email_task)
        while True:
            schedule.run_pending()


def main():
    schedule.every().friday.at("17:25").do(send_email_task)
    i = 0
    if i == 0:
        schedule.every().friday.at("19:25").do(send_email_task)
        i += 1
    while True:
        schedule.run_pending()


if __name__ == '__main__':
    main()
