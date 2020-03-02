from browsermobproxy import Server
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


'''
参考网址：
https://blog.csdn.net/qq_32502511/article/details/101536325
'''
proxy_file = r"E:\data\browsermob-proxy-2.1.4\bin\browsermob-proxy.bat"
try:
    server = Server(proxy_file)
    server.start()
    proxy = server.create_proxy()

    chrome_options = Options()

    chrome_options.add_argument("--proxy-server={0}".format(proxy.proxy))
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36")
    chrome_options.add_argument("authority='www.iesdouyin.com'")
    accept_language = "zh-CN,zh;q=0.9,en;q=0.8";
    chrome_options.add_argument("accept-language="+accept_language)
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation']) # 发爬虫关键字


    driver = webdriver.Chrome(chrome_options=chrome_options)

    url = "http://www.iesdouyin.com/share/user/98569634382?sec_uid=MS4wLjABAAAAukfxyGQmo3HK9N26B8v6SkhCwbtbjEqlThz1U_zxkcI"
    access_url = url
    proxy.new_har("douyin", options={'captureHeaders': True, 'captureContent': True})

    driver.get(access_url)
    time.sleep(6)
    result = proxy.har
    print(result)
    for entry in result['log']['entries']:
        _url = entry['request']['url']
        # print(_url)
        # # 根据URL找到数据接口,这里要找的是 http://git.liuyanlin.cn/get_ht_list 这个接口
        if "_signature" in _url:
            print("=================================>>")
            print(_url)
            _response = entry['response']
            _content = _response['content']
            # 获取接口返回内容
            print(_response)
            print(_content)
            print("<<<============================")
except Exception as e:
    print(e)
    pass
finally:
    server.stop()
    driver.quit()
