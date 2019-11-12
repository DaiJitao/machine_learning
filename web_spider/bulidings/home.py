"""
爬取主要小区信息
"""
from web_spider.bulidings.utils import get_html, parse_html
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


def get_ershoufang_data():
    for page in range(1, 18):
        url = "https://chengde.58.com/chengdexian/ershoufang/pn" + str(page) + "/"

        home_html = get_html(index_url=url)
        parse_html(home_html, out_file="./test" + str(page) + ".xlsx")
        seconds = [60*10.22, 60 * 5.32, 60 * 4.09, 60 * 9.02, 60 * 6.56, 60 * 3.229, 60 * 5.9, 60 * 7.02, 60 * 4.3]
        interval = random.choice(seconds)
        time.sleep(interval)


get_ershoufang_data()
