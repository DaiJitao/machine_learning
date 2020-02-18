import requests
import logging
from io import BytesIO
import json

from PIL import Image

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

url = "http://www.baidu.com"


def get_html(url, params=None, encoding='utf-8'):
    if params:
        response = requests.get(url, params)
    else:
        response = requests.get(url)
    if response.status_code == 200:
        response.encoding = encoding
        return response.text  # 读取文本
    if response.status_code == 403:
        logging.info(url + "禁止访问！")
        return None
    else:
        return None


def get_image(url, params=None):
    if params:
        response = requests.get(url, params)
    else:
        response = requests.get(url)
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        image.save("./test.jpg")
        logging.info("saved test.jpg!")
    if response.status_code == 403:
        logging.info(url + "禁止访问！")
        return None
    else:
        return None


def get_json(url, params=None, encoding='utf-8'):
    if params:
        response = requests.get(url, params)
    else:
        response = requests.get(url)
    if response.status_code == 200:
        response.encoding = encoding
        return response.text  # 读取文本
    if response.status_code == 403:
        logging.info(url + "禁止访问！")
        return None
    else:
        logging.info("status code " + str(response.status_code))
        return None


if __name__ == '__main__':
    image_url = "http://i-2.shouji56.com/2015/2/11/23dab5c5-336d-4686-9713-ec44d21958e3.jpg"
    json_url = "https://github.com/timeline.json"
    print(get_json(json_url))
