import json
import re

if __name__ == '__main__':
    file = "./data/response2.txt"
    with open(file,mode="r",encoding="utf-8") as fp:
        contentJson = fp.read().strip()
        contentDict = json.loads(contentJson, encoding="utf-8")
        print(contentDict["aweme_list"])
        print(len(contentDict["aweme_list"]))
        url = "http://www.iesdouyin.com/share/user/98569634382?sec_uid=MS4wLjABAAAAukfxyGQmo3HK9N26B8v6SkhCwbtbjEqlThz1U_zxkcI&utm_campaign=client_share&app=aweme&utm_medium=ios&tt_from=copy&utm_source=copy"
        number = re.findall(r'share/user/(\d+)', url)
        print(number)

