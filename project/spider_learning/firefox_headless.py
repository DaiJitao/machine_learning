from selenium import webdriver



firefox_options = webdriver.FirefoxOptions()
firefox_options.add_argument("--headless")

url = "https://www.toutiao.com/i6792817006111359495/"

driver_path = r"F:\pycharm_workspace\python3_x\machine_learning\project\spider_learning\driver\geckodriver-v0.26.0-win64\geckodriver.exe"
browser = webdriver.Firefox(firefox_options=firefox_options, executable_path=driver_path)


browser.get(url)
print(browser.page_source)

