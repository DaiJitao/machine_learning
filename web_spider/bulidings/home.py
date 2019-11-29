"""
爬取主要小区信息
"""
from web_spider.bulidings.utils import get_html, parse_html, get_page_num, mkdir, load_xinfang_data
import pandas as pd
import time
import random

#  二手房
old_bulding_url = "https://chengde.58.com/ershoufang/?PGTID=0d100000-01a6-8fa8-4ce8-ee29530827cb&ClickID=2"
# 新房
new_building_url = "https://chengde.58.com/xinfang/?PGTID=0d100000-01a6-8426-001d-5dfa3c6b3702&ClickID=4"

# 承德县二手房
ershoufang_url = "https://chengde.58.com/chengdexian/ershoufang/"
# 承德县新房  "https://chengde.58.com/xinfang/loupan/chengdexian/"
xinfang_url = "https://chengde.58.com/xinfang/loupan/chengdexian/"

seconds = [60 * 11.22, 60 * 6.32, 60 * 9.09, 60 * 7.32, 60 * 9.02, 60 * 12.56, 60 * 6.229, 60 * 5.9, 60 * 9.02,
           60 * 8.13]


def get_ershoufang_data(home_url):
    size = get_page_num(home_url)
    print("获取页数：", size)
    dir_ = time.strftime('%Y-%m-%d-%H_%M', time.localtime(time.time()))
    out_path = "./data/erShoufang/" + dir_ + "/"
    mkdir(out_path)
    time.sleep(seconds[-3])  # 休眠
    for page in range(1, size + 1):
        url = "https://chengde.58.com/chengdexian/ershoufang/pn" + str(page) + "/"
        print("访问：", url)
        home_html = get_html(index_url=url)
        if home_url == None or len(home_html) < 1200:
            print(home_html)
            print(url, "爬取失败！")
        parse_html(home_html, out_file=out_path + "erShouFang" + str(page) + ".xlsx")
        print("saved: ", "erSouFang" + str(page) + ".xlsx")
        interval = random.choice(seconds)
        time.sleep(interval)
    print("采集完毕，一共采集%s页！" % size)


def save_xinfang():
    # 新房---------------------------------------------------------------------------
    time.sleep(60 * 11.633)
    xinfang_name = time.strftime('%Y-%m-%d-%H_%M', time.localtime(time.time()))
    xinfang_url = "https://chengde.58.com/xinfang/loupan/chengdexian/"
    xinfang_html = get_html(index_url=xinfang_url)
    load_xinfang_data(xinfang_html, out_file="./data/xinfang/" + xinfang_name + ".xlsx")


def main():
    # 二手房
    home_url = "https://chengde.58.com/chengdexian/ershoufang/"
    get_ershoufang_data(home_url)
    save_xinfang()


if __name__ == '__main__':
    main()
