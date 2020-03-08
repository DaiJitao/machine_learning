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

UA = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36"
referer = "https://www.iesdouyin.com/share/user/98569634382?sec_uid=MS4wLjABAAAAukfxyGQmo3HK9N26B8v6SkhCwbtbjEqlThz1U_zxkcI"
accept = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3"

options = ChromeOptions()
options.add_argument('lang=zh_CN.UTF-8')
options.add_argument("user-agent=" + UA )
options.add_argument('accept=' + accept)
options.add_argument("accept-language=" + accept_language[0])
options.add_argument('accept-encoding="gzip, deflate, br"')
options.add_argument("upgrade-insecure-requests=1")
options.add_argument('cache-control="max-age=0"')
# options.headless = True
options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 爬虫关键字

file = r"F:\pycharm_workspace\python3_x\machine_learning\web_spider\douyin\VM2841.txt"
with open(file, mode="r", encoding='utf-8') as fp:
    js = fp.read().strip()

user_url = "http://www.iesdouyin.com/share/user/98569634382?sec_uid=MS4wLjABAAAAukfxyGQmo3HK9N26B8v6SkhCwbtbjEqlThz1U_zxkcI"
try:
    driver = webdriver.Chrome(options=options)
    driver.get(user_url)
    time.sleep(6)
    uid = '"98569634382"'
    # js = "var _ = process.argv.splice(2); return arguments[0];"
    js = 'var _bytedAcrawler = __M.require("douyin_falcon:node_modules/byted-acrawler/dist/runtime");' \
         'var nature = _bytedAcrawler.sign('+ uid + ');return nature;'
    # print(js)
    t = driver.execute_script(js)
    print("用户ID: "+uid, "破解加密字段: "+t);
except Exception as e:
    logger.exception(e)
finally:
    driver.quit()
