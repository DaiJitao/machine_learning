import logging
from selenium import webdriver
from pyquery import PyQuery as pq
import requests
import os
import random

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

agents = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5680.400 QQBrowser/10.2.1852.400',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'
 ]
languages = ["zh-CN,zh;q=0.9", "zh-CN,zh;q=0.9,en;q=0.8", "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2"
             ]

accepts = ["text/plain", "application/json, text/javascript", "*/*",
           "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3"
           ]

driver_path = r"F:\pycharm_workspace\python3_x\machine_learning\project\spider_learning\driver\geckodriver-v0.26.0-win64\geckodriver.exe"
firefox_options = webdriver.FirefoxOptions()
firefox_options.add_argument("--headless")


def mkdir(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except Exception as e:
        logging.exception(e)


def load_page(url):
    try:
        browser = webdriver.Firefox(firefox_options=firefox_options, executable_path=driver_path)
        browser.get(url)
        page_source = browser.page_source
        if page_source:
            logging.info(url + " page source loaded successfully")
            return page_source
    except Exception as e:
        logging.exception(e)
    finally:
        browser.close()
        logging.info("firefox browser closed!")


def sub_url(url):
    """视频连接截取"""
    try:
        start_index_p = url.index("?")
        return url[:start_index_p]
    except Exception as e:
        logging.exception(e)


def parse(page_source):
    try:
        logging.info("parsing page source...")
        doc = pq(page_source)
        article_title = doc.find(".article-title").text()
        content_tag = doc.find(".article-content")
        content = article_title + "\n"  # 文章正文
        video_urls = []
        image_urls = []
        for item in content_tag.children():
            doc_item = pq(item)
            if doc_item('p'):
                text = doc_item("p").text()
                if text:
                    content += text.strip() + "\n"
            if doc_item("img"):
                image_url = doc_item("img").attr("src")
                if image_url:
                    image_urls.append(image_url)
                    image_html = '<img src="' + image_url + '" align="center"/>'
                    content += image_html + "\n"
            if doc_item("div"):
                video_box = doc_item("div").find("video")
                # 视频url
                video_url = video_box.attr("src")
                if video_url:
                    video_url = sub_url(video_url)
                    video_urls.append(video_url)
                    # 视频标签
                    video_html = '<video src="' + video_url + '"></video>'
                    content += video_html + "\n"

        logging.info("parsed successfully")
        return content.strip(), image_urls, video_urls
    except Exception as e:
        logging.exception(e)


def load_videos(video_url, save_path, file_name):
    agent = random.choice(agents)
    acl = random.choice(languages)
    accept = random.choice(accepts)

    headers = {'accept-language': acl,
               "Accept": accept,
               "Accept-Encoding": "gzip, deflate, br",
               "User-Agent": agent
               }
    file = save_path + file_name
    try:
        logging.info(video_url + " loading... ")
        response = requests.get(video_url, headers=headers)
        if response.status_code == 200:
            mkdir(save_path)
            with open(file, mode="wb") as fp:
                fp.write(response.content)
            logging.info(file + " loaded successfully!")
        elif response.status_code == 403:
            logging.error(response.status_code)
            logging.error(file + "loaded failedly!")
    except Exception as e:
        logging.exception(e)


def load_article(article_url):
    """
    对外提供的函数
    :param article_url:
    :return:
    """
    page_source = load_page(article_url)
    content, image_urls, video_urls = parse(page_source)
    return content, image_urls, video_urls


def main(article_url):
    save_path = "E:/data/videos/toutiao/"
    # article_url = "https://www.toutiao.com/i6795123939421979139/"# "https://www.toutiao.com/i6795123896686215692/" # "https://www.toutiao.com/i6790247153152295432/"
    content, image_urls, video_urls = load_article(article_url)
    start_index = article_url.index("/i")
    if article_url.endswith("/"):
        video_name = article_url[start_index + 2:-1] + ".mp4"
    else:
        video_name = article_url[start_index + 2:] + ".mp4"
    for url in video_urls:
        load_videos(video_url=url, save_path=save_path, file_name=video_name)


if __name__ == '__main__':
    #  "https://www.toutiao.com/i6792822936743969287/" #
    # "https://www.toutiao.com/i6792817006111359495/" "https://www.toutiao.com/i6792817299754582541/" "https://www.toutiao.com/i6792820767974228493/" #
    article_url = "https://www.toutiao.com/i6793908353828389379/"  # "https://www.toutiao.com/i6795123939421979139/"
    main(article_url)
