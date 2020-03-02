import json
import re
import urllib.parse as parse
import time

url_file = "./data/js_urls"

def url_query():
    with open(url_file) as file:
        lines = file.readlines()
        for url in lines:
            print(parse.urlparse(url.strip()).query)

def main():
    file = "./data/r3.txt"
    with open(file,mode="r",encoding="utf-8") as fp:
        string = fp.read().strip()
        contentJson= json.loads(string, encoding="utf-8")
        print(len(contentJson["aweme_list"]))
        max_cursor1 = 0
        aweme_list = contentJson.get("aweme_list")
        for index, aweme in enumerate(aweme_list):
            if max_cursor1 == 0:
                max_cursor2 = int(time.time()) - index * 2000
            else:
                max_cursor2 = int(max_cursor) / 1000 + index * 2000
            creat_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(max_cursor2))
            logger.info("正在采集用户-->> " + nick_name)
            # 下载视频
            self._join_download_queue(aweme, nick_name, creat_time, target_folder, user_id, type, url_items)


if __name__ == '__main__':
    main()




