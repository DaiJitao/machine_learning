from browsermobproxy import Server  ,client# pip install browsermob-proxy
from selenium import webdriver
import requests

#
from selenium.webdriver.chrome.options import Options
#实现规避检测
from selenium.webdriver import ChromeOptions

from selenium.webdriver.firefox.options import Options as FirefoxOptions
import time
from web_spider.demo.common import accept_language, USER_AGENTS, proxy_file, get_logger

fireFox_driver = "F:\pycharm_workspce\dai_github\ml_test1\machine_learning\project\spider_learning\driver\geckodriver-v0.26.0-win64\geckodriver.exe"
logger = get_logger()

def get_json(url, params=None, encoding='utf-8'):
    if params:
        response = requests.get(url,headers=params)
    else:
        response = requests.get(url)
    if response.status_code == 200:
        response.encoding = encoding
        return response.text  # 读取文本
    if response.status_code == 403:
        logger.info(url + "禁止访问！")
        return None
    else:
        logger.info("status code " + str(response.status_code))
        return None


def get_signature_url(user_url):
    try:
        # 代理服务
        server = Server(proxy_file)
        server.start()
        proxy = server.create_proxy()

        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--proxy-server={0}".format(proxy.proxy))
        chrome_options.add_argument("user-agent=" + USER_AGENTS[0])
        chrome_options.add_argument("accept-language=" + accept_language[0])

        # 规避检测
        option = ChromeOptions()  # FirefoxOptions()
        option.add_experimental_option('excludeSwitches', ['enable-automation'])  # 爬虫关键字

        driver = webdriver.Chrome(chrome_options=chrome_options, options=option)

        proxy.new_har("douyin", options={'captureHeaders': True, 'captureContent': True})

        logger.info("原始URL {}".format(url))
        driver.get(user_url)
        time.sleep(3)
        result = proxy.har  # 获取HAR
        # print(result)
        for entry in result['log']['entries']:
            _url = entry['request']['url']
            # print(_url)
            # # 根据URL找到数据接口,这里要找的是 http://git.liuyanlin.cn/get_ht_list 这个接口
            if "_signature" in _url:
                logger.info("获取到用户第一个数据请求接口---------->>>\n{}".format(_url))
                return _url
                # print(_url)
                _response = entry['response']
                _content = _response['content']
                # 获取接口返回内容
                # print(_content)
    except Exception as e:
        logger.exception(e)
        pass
    finally:
        server.stop()
        driver.quit()


if __name__ == '__main__':
    # 账号
    url = "http://www.iesdouyin.com/share/user/98569634382?sec_uid=MS4wLjABAAAAukfxyGQmo3HK9N26B8v6SkhCwbtbjEqlThz1U_zxkcI"
    data_url = get_signature_url(url)
    headers = {
        "User-Agent":USER_AGENTS[0],
        "accept-language":accept_language[0],
        "upgrade-insecure-requests":"1",
        "accept":accept[0]

    }

