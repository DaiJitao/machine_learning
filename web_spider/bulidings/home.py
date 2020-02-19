"""
爬取主要小区信息
"""
from web_spider.bulidings.utils import get_html, parse_html, get_page_num, mkdir, load_xinfang_data
import time
import random
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

#  二手房
old_bulding_url = "https://chengde.58.com/ershoufang/?PGTID=0d100000-01a6-8fa8-4ce8-ee29530827cb&ClickID=2"
# 新房
new_building_url = "https://chengde.58.com/xinfang/?PGTID=0d100000-01a6-8426-001d-5dfa3c6b3702&ClickID=4"

# 承德县二手房
ershoufang_url = "https://chengde.58.com/chengdexian/ershoufang/"
# 承德县新房  "https://chengde.58.com/xinfang/loupan/chengdexian/"
# xinfang_url = "https://chengde.58.com/xinfang/loupan/chengdexian/"

seconds = [60 * 11.22, 60 * 6.32, 60 * 9.09, 60 * 7.32, 60 * 9.02, 60 * 12.56, 60 * 6.229, 60 * 5.9, 60 * 9.02,
           60 * 8.13]


def get_ershoufang_data(home_url, page_url_sub, out_path):
    size = get_page_num(home_url)
    logging.info("获取页数：" + str(size))
    dir_ = time.strftime('%Y-%m-%d-%H_%M', time.localtime(time.time()))
    out_path = out_path + dir_ + "/"
    mkdir(out_path)
    time.sleep(random.choice(seconds))  # 休眠
    for page in range(1, size + 1):
        # url = "https://chengde.58.com/chengdexian/ershoufang/pn" + str(page) + "/"
        url = page_url_sub + str(page) + "/"
        logging.info("访问：" + url)
        home_html = get_html(index_url=url)
        if home_url == None or len(home_html) < 1200:
            logging.error(home_html)
            logging.error(url + "爬取失败！")
        parse_html(home_html, out_file=out_path + "erShouFang" + str(page) + ".xlsx")
        logging.info("saved successfully " + "erShouFang" + str(page) + ".xlsx")
        interval = random.choice(seconds)
        time.sleep(interval)
    logging.info("二手房采集完毕，一共采集" + str(size) + "页！")


def save_xinfang(xinFang_url, out_path):
    # 新房------------
    logging.info("进入等待区...，开始采集新房 " + xinFang_url)
    time.sleep(60 * 11.633)
    xinfang_name = time.strftime('%Y-%m-%d-%H_%M', time.localtime(time.time()))
    xinfang_html = get_html(index_url=xinFang_url)
    mkdir(out_path)
    load_xinfang_data(xinfang_html, out_file=out_path + xinfang_name + ".xlsx")
    logging.info("新房采集完毕 " + out_path + xinfang_name + ".xlsx 文件已经保存！")


def main():
    urls = {
        "chengdexian_ershoufang": "https://chengde.58.com/chengdexian/ershoufang/",  # 二手房 承德县
        "chengdexian_xinfang": "https://chengde.58.com/xinfang/loupan/chengdexian/",  # 新房 承德县
        "chengdexian_page_url_sub": "https://chengde.58.com/chengdexian/ershoufang/pn" #二手房翻页
    }
    home_url = urls['chengdexian_ershoufang']
    get_ershoufang_data(home_url,
                        page_url_sub=urls['chengdexian_page_url_sub'], out_path="./data/chengDeXian/erShouFang/")
    xinFang_url = urls['chengdexian_xinfang']
    save_xinfang(xinFang_url, out_path="./data/chengDeXian/xinFang/")


if __name__ == '__main__':
    main()
