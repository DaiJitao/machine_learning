from selenium import webdriver

option = webdriver.ChromeOptions()
option.add_argument("headless")

def page(url):
    try:
        driver = webdriver.Chrome(chrome_options=option)
        driver.get(url)
        page_src = driver.page_source
        print(page_src)
    except Exception as e:
        print(e)
    finally:
        driver.close()



if __name__ == '__main__':
    url = "http://www.baidu.com"
    page(url)