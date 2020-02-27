from selenium import webdriver
from pprint import pprint
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time

capabilities = DesiredCapabilities.CHROME
capabilities['loggingPrefs'] = {'browser': 'ALL'}


class Chrome_headless:
    """无头的Chrome浏览器"""

    def __init__(self):
        self.chromeOptions = webdriver.ChromeOptions()  # chrome 选项设置对象
        # self.chromeOptions.add_argument('headless')  # 设置无界面
        # self.chromeOptions.add_argument('window-size=1200x600') # 虚拟屏幕大小
        self.wb = webdriver.Chrome(chrome_options=self.chromeOptions,
                                   desired_capabilities=capabilities)  # 创建chrome 浏览器对象

    def get_parse(self, url):
        pprint(dir(self.wb))

        self.wb.get(url)
        # self.wb.set_window_size(1366, 768) # 设置请求之后的虚拟界面大小，以便获取页面的内容。
        html = self.wb.page_source
        print(self.wb.log_types)
        # print(html)
        # driver.get_log('browser')
        # driver.get_log('driver')
        # driver.get_log('client')
        # driver.get_log('server')
        print("log\n", self.wb.get_log('browser'))


if __name__ == '__main__':
    url = "http://www.iesdouyin.com/share/user/98569634382?sec_uid=MS4wLjABAAAAukfxyGQmo3HK9N26B8v6SkhCwbtbjEqlThz1U_zxkcI"

    try:
        chromeOptions = webdriver.ChromeOptions()  # chrome 选项设置对象
        wb = webdriver.Chrome(chrome_options=chromeOptions)
        wb.get(url)

        time.sleep(10)
    finally:
        wb.close()
