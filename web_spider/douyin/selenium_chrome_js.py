from browsermobproxy import Server  # pip install browsermob-proxy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import time
from web_spider.demo.common import accept_language, USER_AGENTS, proxy_file, get_logger, accept
import requests
from urllib.parse import urlparse
import json

logger = get_logger()

options = ChromeOptions()  # FirefoxOptions()
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


user_url = "http://www.iesdouyin.com/share/user/98569634382?sec_uid=MS4wLjABAAAAukfxyGQmo3HK9N26B8v6SkhCwbtbjEqlThz1U_zxkcI"
try:
    driver = webdriver.Chrome(options=options)
    driver.get(user_url)
    time.sleep(3)
    js = "return  t._signature;"
    t = driver.execute_script(js)
    print(t)
except Exception as e:
    logger.exception(e)
finally:
    driver.quit()
