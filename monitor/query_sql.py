import configparser


cf = configparser.ConfigParser()
cf.read("./config.ini")
types = cf.sections()

email = types[4]
interval = cf.get(email, 'inerval_day')
if interval:
    inerval_day = interval
else:
    inerval_day = 7

# 查询间隔 日期相减
query = "SELECT  total_data,cycle_type, cycle_num,  account_total,article_cycle_num,  article_total, article_cycle_num,  article_text_total, article_text_cycle_num,  article_micro_total,article_micro_cycle_num,  article_video_total, article_video_cycle_num,  update_total, update_cycle_num,  updata_micro_total,update_micro_cycle,  update_text_total,update_text_cycle,  update_video_total, update_video_cycle,  comment_total, comment_cycle,  video_total,video_cycle,  time_insert " \
        "FROM ##table## " \
        "WHERE date_format(time_insert, '%Y%m%d') = date_format(date_sub(current_timestamp, INTERVAL {} DAY), '%Y%m%d') order by total_data desc limit 1;".format(inerval_day)


def get_sql():
    return query

if __name__ == '__main__':
    print(get_sql())
