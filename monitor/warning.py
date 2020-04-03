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


def gen_content(sql_result, type_name):
    '''
        组合邮件内容
    :param sql_result:
    :param type:
    :return:
    '''
    if type_name == "toutiao":
        type = "头条号"
    elif type_name == "douyin":
        type = "抖音号"
    result = []
    cycle_type = sql_result['cycle_type']  # 周期量的类型
    # strftime('%Y-%m-%d %H:%M:%S')
    time_insert = sql_result['time_insert'] # 终点时间
    time_start = time_insert - datetime.timedelta(minutes=int(cycle_type))
    if type_name == "toutiao":
        time_scope = "报告时间:\t" + time_insert.strftime('%Y{0}%m{1}%d{2} %H:%M').format('/', '/', '/')
        result.append(time_scope)
        result.append("-" * 66)

    # cycle_type = "周期的类型:每隔" + cycle_type + "分钟"
    # result.append(cycle_type)
    # 计算数据总量
    total_data = sql_result['total_data']
    total_data_str = type + "数据采集量:\t" + str(total_data) + "\t条"
    result.append(total_data_str)
    # cycle_num = sql_result["cycle_num"]
    # cycle_str = "周期量:" + str(cycle_num)
    # result.append(cycle_str)
    # 账号总量

    account_total = sql_result['account_total']
    account_srt = type + "账号信息采集量:\t" + str(account_total) + "\t条"
    result.append(account_srt)
    # account_cycle_num = sql_result["account_cycle_num"]
    # account_cycle_str = "账号数据周期量：" + str(account_cycle_num)
    # result.append(account_cycle_str)
    # 文章
    if type_name == "toutiao":
        article_total = sql_result['article_total']
        result.append(type + "文章采集量:\t" + str(article_total) + "\t条")
    # article_cycle_num = sql_result['article_cycle_num']
    # result.append("文章数据周期量:" + str(article_cycle_num))

    # micro
    if type_name == "toutiao":
        article_micro_total = sql_result['article_micro_total']
        result.append(type + "微头条采集量:\t" + str(article_micro_total) + "\t条")
    # article_micro_cycle_num = sql_result['article_micro_cycle_num']
    # result.append("微头条数据周期量:" + str(article_micro_cycle_num))

    # article_video_total = sql_result['article_video_total']
    # result.append(type + "视频数据总量:" + str(article_video_total) + "\t条")
    # article_video_cycle_num = sql_result['article_video_cycle_num']
    # result.append("视频数据周期量:" + str(article_video_cycle_num))

    update_total = sql_result['update_total']
    result.append(type + "更新信息量:\t" + str(update_total) + "\t条")
    # update_cycle_num = sql_result['update_cycle_num']
    # result.append("更新数据周期量:" + str(update_cycle_num))

    if type_name == "toutiao":
        comment_total = sql_result['comment_total']
        result.append(type + "评论数据总量:\t" + str(comment_total) + "\t条")
    # comment_cycle = sql_result['comment_cycle']
    # result.append("评论数据周期量:" + str(comment_cycle))

    if type_name == "douyin":
        video_cycle = sql_result['video_total']
        result.append(type + "视频采集量:\t" + str(video_cycle) + "\t条")
        # video_cycle = sql_result['video_cycle']
    # result.append("视频信息数据总量:" + str(video_cycle))

    result = "\n".join(result)
    return result


def send_email_all():
    receivers = cf.get(email, 'receivers')  # 动态获取邮件接受者
    receivers = receivers.split(",")
    logger.info("receivers:{}".format(receivers))
    try:
        mysql = MySQL(user=user, pwd=password, host=host, db=db, tb=toutiao_table)
        sql_result = mysql.latest_data()
        result_toutiao = gen_content(sql_result, "toutiao")
        mysql = MySQL(user=user, pwd=password, host=host, db=db, tb=douyin_tb)
        sql_result = mysql.latest_data()
        result_douyin = gen_content(sql_result, "douyin")
        t = "\n" + "-" * 66 + "\n"
        result = "自媒体采集系统采集情况报告：\n" + "-" * 66 + "\n" \
                 + result_toutiao + t + result_douyin
        send_email(smtp_server, receivers=receivers, email_content=result)

    except Exception as e:
        traceback.print_exc()
        logger.error(e)
        logger.exception("{}".format(e))


def send_email_task():
    t = Thread(target=send_email_all)
    t.start()


def main():
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


if __name__ == '__main__':
    main()
