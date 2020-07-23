from appium import webdriver
import time
import random

desired_caps = {
    'platformName': 'Android',
    'deviceName': 'MI 9',
    'appPackage': 'com.ss.android.ugc.aweme.lite',
    'appActivity': 'com.ss.android.ugc.aweme.splash.SplashActivity'
}

# 指定Appium Server
server = 'http://localhost:4723/wd/hub'
# 新建一个driver
driver = webdriver.Remote(server, desired_caps)

# 获取模拟器/手机的分辨率(px)
width = driver.get_window_size()['width']
height = driver.get_window_size()['height']
print(width, height)

# c = driver.get_clipboard()
# t = driver.get_clipboard_text()

# start_x = width // 2  # 屏幕宽度中心点
# start_y = height // 3 * 2  # 屏幕高度从上开始到下三分之二处
# distance = height // 2  # 滑动距离：屏幕高度一半的距离

time_ = [600, 580, 800, 700, 900, 480, 750]


def search():
    time.sleep(3)
    print("开始点击【好的】")
    # [170,971][730,1067]
    driver.tap([(170, 971), (730, 1067)], 800)
    time.sleep(3)
    print('关闭【红包弹窗】')
    driver.tap([(660, 400), (50, 490)], 800)
    time.sleep(3)
    print("开始滑动")
    driver.swipe(start_x=400, start_y=1404, end_x=473, end_y=875)
    time.sleep(3)
    print("开始点击【搜索】")
    searchBtn = driver.find_element_by_id("com.ss.android.ugc.aweme.lite:id/b0x")  # 获取搜索按钮
    time.sleep(1)
    searchBtn.click()  # 点击搜索
    time.sleep(2)
    driver.find_element_by_id("com.ss.android.ugc.aweme.lite:id/ahx").send_keys("新华网")
    time.sleep(2)
    print("点击第一个列表")
    driver.tap([(96, 181), (186, 222)], random.choice(time_))
    time.sleep(2)
    print("点击用户")
    driver.tap([(346, 154), (503, 234)], random.choice(time_))
    print(driver.page_source)

    # driver.tap([(816,58),(888,130)], 600)
    time.sleep(1)

    textViews = driver.find_element_by_id("com.ss.android.ugc.aweme.lite:id/dpl")
    print()
    print(textViews)
    print('<<<==============================================')
    for i in textViews:
        print("i=\n{}".format(i))
        print('*' * 20)


'''获取视频连接'''


def tap():
    time.sleep(6)
    print("开始点击【好的】")
    # [170,971][730,1067]
    driver.tap([(170, 971), (730, 1067)], 800)
    time.sleep(3)
    print('关闭【红包弹窗】')
    driver.tap([(660, 400), (50, 490)], 800)

    time.sleep(3)
    print("开始滑动")
    driver.swipe(start_x=400, start_y=1404, end_x=473, end_y=875)
    print(driver.page_source)
    time.sleep(5)
    print("开始点击【分享】")
    driver.tap([(799, 1192), (879, 1272)], 600)
    time.sleep(3)
    print("点击复制分享链接")
    driver.tap([(740, 1317), (836, 1413)], 700)
    time.sleep(2)
    c = driver.get_clipboard()
    t = driver.get_clipboard_text()
    print("clipboard={}, \n text={}".format(c, t))
    time.sleep(1)
    # print(driver.page_source)


if __name__ == '__main__':
    # 点击一次屏幕
    # tap()
    search()
    print("============>")


def info():
    return driver.page_source

# print(info())
