from selenium import webdriver
import pickle
import time
import requests
from web_spider.rumor import config
from web_spider.rumor.utils import save_data_txt
import random

# 不实信息
url = "https://service.account.weibo.com/?type=5&status=0"

headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           "Accept-Encoding": "gzip, deflate, br",
           "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
           "Connection": "keep-alive",
           "Cookie": config.Cookie,
           "Host": "s.weibo.com",
           "Referer": "https://service.account.weibo.com/?type=5&status=0",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0"
           }


class WeiBo(object):
    def __init__(self, username, password, login_url):
        self.username = username
        self.pwd = password
        self.driver = webdriver.Chrome()
        self.driver.get(url=login_url)
        self.set_cookie()
        self.is_login()

    def is_login(self):
        self.driver.refresh()
        html = self.driver.page_source
        if html.find(self.username) == -1:  # 利用用户名判断是否登陆
            # 没登录 ,则手动登录
            self.login()

        else:
            # 已经登录  尝试访问搜索记录，可以正常访问
            self.driver.get(url='http://i.baidu.com/my/history')
            time.sleep(30)  # 延时看效果

    def login(self):
        '''登陆'''
        time.sleep(60)  # 等待手动登录
        self.driver.refresh()
        self.save_cookie()

    def save_cookie(self):
        '''保存cookie'''
        # 将cookie序列化保存下来
        pickle.dump(self.driver.get_cookies(), open("cookies.pkl", "wb"))

    def set_cookie(self):
        '''往浏览器添加cookie'''
        '''利用pickle序列化后的cookie'''
        try:
            cookies = pickle.load(open("cookies.pkl", "rb"))
            for cookie in cookies:
                cookie_dict = {
                    # "domain": ".baidu.com",  # 火狐浏览器不用填写，谷歌要需要
                    'name': cookie.get('name'),
                    'value': cookie.get('value'),
                    "expires": "",
                    'path': '/',
                    'httpOnly': False,
                    'HostOnly': False,
                    'Secure': False}
                self.driver.add_cookie(cookie_dict)
        except Exception as e:
            print(e)


def get_html(url, headers, encoding='utf-8', try_times=3):
    # 重试三次
    for i in range(try_times):
        html = get_page(url, encoding=encoding, headers=headers)
        if html != None:
            return html
        times = [1, 3, 4, 2, 1.5]
        time.sleep(random.choice(times))
    return html



def get_page(url, encoding, headers):
    response = requests.get(url, headers)
    if response.status_code == 200:
        response.encoding = encoding  # 解决中文乱码 utf-8 'gb2312'
        html = response.text
    elif response.status_code == 403:
        print("无法获取网页")
        html = None
    return html


if __name__ == '__main__':
    url = "https://service.account.weibo.com/?type=5&status=0"
    html = get_html(url,headers=headers)
    save_data_txt("./html/","index.html",data=html)
