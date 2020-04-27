import configparser
import datetime
import schedule
from threading import Thread

cf = configparser.ConfigParser()
cf.read("./config.ini")
data = cf.sections()


d = {'article_total': 0, 'article_cycle_num': 0, 'video_cycle': 0, 'article_micro_cycle_num': 0, 'video_total': 0, 'total_data': 110, 'article_text_cycle_num': 0, 'update_cycle_num': 0, 'time_insert': datetime.datetime(2020, 3, 13, 13, 22, 18), 'article_video_cycle_num': 0, 'update_micro_cycle': 0, 'update_total': 0, 'update_text_total': 0, 'time_update': datetime.datetime(2020, 3, 13, 13, 22, 18), 'article_micro_total': 0, 'comment_cycle': 0, 'account_cycle_num': 0, 'comment_total': 0, 'update_video_cycle': 0, 'cycle_num': 110, 'updata_micro_total': 0, 'update_text_cycle': 0, 'update_video_total': 0, 'article_text_total': 0, 'article_video_total': 0, 'account_total': 0, 'cycle_type': '1'}


def print_task():
    t = Thread(target=print_demo)
    t.start()

def print_demo():
    print("demo")

def main():
    schedule.every().friday.at("18:40").do(print_task)
    while True:
        schedule.run_pending()




if __name__ == '__main__':
    main()
