'''

'''
from pyquery import PyQuery as pq
from selenium import webdriver
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def load_page(article_url):
    try:
        driver = webdriver.PhantomJS()
        logging.info("accessing " + article_url)
        driver.get(article_url)
        page_source = driver.page_source
        if page_source:
            logging.info("page source loaded sucessfully!")
            return page_source
    except Exception as e:
        logging.exception(e)
    finally:
        driver.quit()
        logging.info("driver exited!")


def sub_url(url):
    try:
        start_index_p = url.index("?")
        return url[:start_index_p]
    except Exception as e:
        logging.exception(e)


def parse(page_source):
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
            video_url = sub_url(video_url)
            if video_url:
                video_urls.append(video_url)
                # 视频标签
                video_html = '<video src="' + video_url + '"></video>'
                content += video_html + "\n"

    return content.strip(), image_urls, video_urls


def load_article(article_url):
    """
    对外提供的函数
    :param article_url:
    :return:
    """
    page_source = load_page(article_url)
    content, image_urls, video_urls = parse(page_source)
    return content, image_urls, video_urls


def main():
    article_url = "https://www.toutiao.com/i6792817006111359495/"
    content, image_urls, video_urls = load_article(article_url)
    print(content)
    print(image_urls)
    print(video_urls)


if __name__ == '__main__':
    main()