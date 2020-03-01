from browsermobproxy import Server  # pip install browsermob-proxy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import time
from web_spider.demo.common import accept_language, USER_AGENTS, proxy_file, get_logger, accept
import requests
from urllib.parse import urlparse
import json

'''
参考网址：
https://blog.csdn.net/qq_32502511/article/details/101536325
'''
fireFox_driver = "F:\pycharm_workspce\dai_github\ml_test1\machine_learning\project\spider_learning\driver\geckodriver-v0.26.0-win64\geckodriver.exe"
logger = get_logger()


def get_json(url, headers=None, encoding='utf-8'):
    if headers:
        response = requests.get(url, headers=headers)
    else:
        response = requests.get(url)
    if response.status_code == 200:
        # response.encoding = encoding
        return response.content().decode("utf-8")  # 读取文本
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

        options = ChromeOptions()  # FirefoxOptions()
        options.add_argument("--proxy-server={0}".format(proxy.proxy))
        options.add_argument('--disable-gpu')
        options.add_argument('lang=zh_CN.UTF-8')
        options.add_argument("user-agent=" + USER_AGENTS[0])
        options.add_argument('accept=' + accept[0])
        options.add_argument("accept-language=" + accept_language[0])
        options.add_argument('accept-encoding="gzip, deflate, br"')
        options.add_argument("upgrade-insecure-requests=1")
        options.add_argument('cache-control="max-age=0"')
        # options.headless = True
        options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 爬虫关键字

        # webdriver.Firefox(options,executable_path=fireFox_driver)  # # webdriver.Firefox(firefox_options=chrome_options)#
        driver = webdriver.Chrome(options=options)
        proxy.new_har("douyin", options={'captureHeaders': True, 'captureContent': True})
        logger.info("原始URL {}".format(url))
        driver.get(user_url)
        time.sleep(6)
        result = proxy.har  # 获取HAR
        # print(result)
        for entry in result['log']['entries']:
            _url = entry['request']['url']
            # print(_url)
            # # 根据URL找到数据接口,这里要找的是 http://git.liuyanlin.cn/get_ht_list 这个接口
            if "_signature" in _url:
                logger.info("获取到用户第一个数据请求接口------>>>\n{}".format(_url))
                return _url
                # print(_url)
                # _response = entry['response']
                # _content = _response['content']
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
        "User-Agent": USER_AGENTS[0],
        "accept-language": accept_language[0],
        "upgrade-insecure-requests": "1",
        "accept": accept[0],
        "lang": "zh_CN.UTF-8",
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        "accept-encoding": "gzip, deflate, br",
        "cookie": "_ga=GA1.2.637118698.1582697580; _gid=GA1.2.129343412.1583039039"
    }
    p = urlparse(data_url)
    user_video_url = "https://" + p.hostname + p.path
    temp = [part.split("=") for part in p.query.split("&")]
    user_video_params = {part[0]: part[1] for part in temp}
    print(user_video_params)

    res = requests.get(user_video_url, headers=headers, params=user_video_params, timeout=4)
    print(dir(res))
    print(res.json)
    contentJson = json.loads(res.content.decode())
    print(contentJson)
