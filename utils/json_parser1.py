import json
import re
import urllib.parse as parse

url_file = "./data/js_urls"

def main():
    file = "./data/r3.txt"
    with open(file,mode="r",encoding="utf-8") as fp:
        contentJson = fp.read().strip()
        contentDict = json.loads(contentJson, encoding="utf-8")
        print(contentDict["aweme_list"])
        print(len(contentDict["aweme_list"]))
        url = "http://www.iesdouyin.com/share/user/98569634382?sec_uid=MS4wLjABAAAAukfxyGQmo3HK9N26B8v6SkhCwbtbjEqlThz1U_zxkcI&utm_campaign=client_share&app=aweme&utm_medium=ios&tt_from=copy&utm_source=copy"
        number = re.findall(r'share/user/(\d+)', url)
        print(number)

if __name__ == '__main__':
    with open(url_file) as file:
        lines = file.readlines()
        for url in lines:
            print(parse.urlparse(url.strip()).query)



