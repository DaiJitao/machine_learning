import requests
from pyquery import PyQuery as pq
import pandas as pd
from requests.exceptions import RequestException
import time
import os
import csv
from urllib.parse import urlparse
from multiprocessing import cpu_count
import random

times = [8.96 * 60, 11.3 * 50, 12.602 * 60, 10.2 * 60, 7.56 * 60, 5.56 * 60, 12.62 * 60, 9.33 * 60, 60 * 6.16,
         8 * 7.58, ]
cpu_cores = cpu_count()
agents = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0",
          "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
          "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
          'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362',
          'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0',
          'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; rv:11.0) like Gecko',
          'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5680.400 QQBrowser/10.2.1852.400']
languages = ["zh-CN,zh;q=0.9", "zh-CN,zh;q=0.9,en;q=0.8", "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2"]

accepts = ["text/plain", "application/json, text/javascript", "*/*",
           "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3"]


def __get_page(index_url, encoding, headers):
    # print("access url: ", index_url)
    agent = random.choice(agents)
    acl = random.choice(languages)
    accept = random.choice(accepts)
    try:
        response = requests.get(index_url, headers=headers)
        if response.status_code == 200:
            response.encoding = encoding  # 解决中文乱码 utf-8 'gb2312'
            return response.text
        elif response.status_code == 403:
            return None
        else:
            return None
    except RequestException as e:
        print(e)
        return None


def get_html(index_url, encoding="utf-8", try_times=3, headers=None):
    '''
    带请求头的数据抓取
    默认重试次数3.
    '''

    for i in range(try_times):
        if headers == None:
            html = __get_page(index_url=index_url, encoding=encoding)
        else:
            html = __get_page(index_url=index_url, encoding=encoding, headers=headers)
        if html != None:
            return html
        breakTime = random.choice(times)
        time.sleep(breakTime)


def mkdir(path):
    try:
        os.makedirs(path)
    except:
        pass


def save_data_txt(file_path, name, data):
    if file_path.endswith("/"):
        file = file_path + name
    else:
        file = file_path + "/" + name
    with open(file, 'w',encoding='utf-8') as file:
        file.write(data)


def to_csv(path, file_name, data):
    """
    :param path: 保存路径
    :param file_name: 文件名字
    :param data: [ ["name", "age"] ]
    :return:
    """
    if data == None:
        print("无数据保存")
    else:
        with open(path + file_name, mode='w', newline='', encoding='utf-8') as csvfile:
            csv_write = csv.writer(csvfile, dialect="excel")
            # csv_write.writerow(["name", "age"])
            for news in data:
                csv_write.writerow(news)


def all_index(data, v):
    result = []
    count = 0
    for value in data:
        if value == v:
            result.append(count)
        count += 1
    return result


def load_data_from_txt(file):
    result = set()
    with open(file, mode="r") as text:
        for line in text.readlines():
            tmp = line.strip()
            path = urlparse(tmp).path
            indexes = all_index(path, "/")
            start, second = indexes[0], indexes[1]
            channel = path[start + 1: second]
            result.add(channel)
    print(result)


def formate_time(time):
    if time < 10:
        return "0" + str(time)
    return str(time)


def group_thread(size):
    gs = []
    interval = (size // cpu_cores)
    plus = size % cpu_cores
    for i in range(0, cpu_cores):
        if i == (cpu_cores - 1) and plus != 0:
            gs.append([end, size])
        else:
            start = i * interval
            end = start + interval
            gs.append([start, end])
    return gs


def get_page_num(url):
    try:
        home_html = get_html(index_url=url)
        doc = pq(home_html)
        li_list = doc.find(".pager a")
        a_list = [a for a in li_list.items()]
        # print(a_list)
        size = a_list[-2].text().strip()
        return int(size)
    except:
        return 17


def get_xinfang_page_num(url):
    pass


def load_xinfang_data(html, out_file):
    doc = pq(html)
    links = []
    titles = []
    prices = []
    addresses = []
    huxings = []
    tags = []
    try:
        loads = doc.find(".key-list.imglazyload")
        item_mods = loads.find(".item-mod")
        for item_mod in item_mods.items():
            infos = item_mod.find(".infos")
            title_el = infos.find(".lp-name")
            title = title_el.text().strip()
            link = title_el.attr('href')
            # 地址
            address = infos.find(".address").text().strip()
            huxing = infos.find(".huxing").text().strip()  # huxing
            tag = infos.find(".tag-panel").text().strip()  # tag-panel
            price = item_mod.find(".favor-pos").text().strip()
            links.append(link)
            titles.append(title)
            addresses.append(address)
            huxings.append(huxing)
            tags.append(tag)
            prices.append(price)

    except:
        pass

    writer = pd.ExcelWriter(out_file, engine="xlsxwriter", options={'strings_to_urls': False})
    data = pd.DataFrame(
        {'title': titles, "地址": addresses, "楼盘价格": prices, "户型": huxings, "标签": tags, "链接": links})
    data.to_excel(writer, index=False)
    writer.save()


def parse_html(html, out_file):
    doc = pq(html)
    links = []
    titles = []
    baseinfos = []
    jjrinfos = []
    sum_s = []
    units = []
    times = []
    try:
        li_list = doc.find(".house-list-wrap li")
        for li in li_list.items():
            title_element = li.find(".title")
            a = title_element.find('a[target="_blank"]')
            link = a.attr('href')  # 获取连接
            if ":" not in link[:6]:
                link = "https:" + link
            title = title_element.text().strip()
            baseinfo = li.find(".baseinfo").text().strip()
            jjrinfo = li.find(".jjrinfo").text().strip()
            sum_ = li.find(".price .sum").text().strip()
            unit = li.find(".price .unit").text().strip()
            try:
                time = li.find(".time").text().strip()
            except:
                time = "广告"
            links.append(link)
            titles.append(title)
            baseinfos.append(baseinfo)
            jjrinfos.append(jjrinfo)
            sum_s.append(sum_)
            units.append(unit)
            times.append(time)
    except:
        pass

    writer = pd.ExcelWriter(out_file, engine="xlsxwriter", options={'strings_to_urls': False})
    data = pd.DataFrame(
        {'title': titles, "基本信息": baseinfos, "总价": sum_s, "单价": units, "发布时间": times, "经纪人信息": jjrinfos,
         "链接": links})
    data.to_excel(writer, index=True)
    writer.save()
