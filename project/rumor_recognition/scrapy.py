from project.rumor_recognition.utils import get_html, to_csv
from pyquery import PyQuery as pq
import pandas as pd

headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           "Accept-Encoding": "gzip, deflate",
           "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
           "Connection": "keep-alive",
           "Cookie": "counterRumour.session.id=e1642921a9024f5390babd5e61ab4ceb; JSESSIONID=AF12B98C7F59CD56AC76CF11F3EBB35C; pageNo=9; pageSize=30",
           "Host": "10.125.9.199:8080",
           "Origin": "http://10.125.9.199:8080",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0"
           }


def load_rumor_index():
    '''
    下载谣言地址
    :return:
    '''
    file = open("./data/rumors_urls.txt", encoding="utf-8", mode="w")
    count = 1
    for pageNo in range(1, 201):
        url = "http://10.125.9.199:8080/a/disrumour/dispelRumour/?pageNo=" + str(
            pageNo) + "&pageSize=50&orderBy=PUBLISHTIME&order=DESC&isSortField=0&" \
                      "title=&source.id=&source.name=&checkStatus=&type=&city.code=&city.name=&beginReleaseTime=&endReleaseTime="

        html = get_html(url, headers=headers)
        if html == None:
            print("无效访问" + url)
        else:
            doc = pq(html)
            tr_s = doc.find("tbody tr")
            for row in tr_s.items():
                element_temp = [e for e in row.find("td").items()][1]
                link = element_temp.find("a").attr("link")
                file.write(link + "\n")
                if count == 500:
                    file.flush()
                count += 1

    file.close()


def get_ulrs():
    with open("./data/rumors_urls.txt", mode='r',encoding="utf-8") as f:
        for line in f.readlines():
            yield line.strip()

if __name__ == '__main__':
    url2 = "http://10.125.9.199:8080/a/disrumour/dispelRumour/view?id=b71226ed88554794b732d0e268818648"
    urls = ["http://10.125.9.199:8080/a/disrumour/dispelRumour/view?id=06eb1a64cdce422f853f4bb83e521460"]

    out_file = "./data/results.xlsx"
    links = []  # 原文链接
    titles = []  # 辟谣主题
    tags = []  # 辟谣标签
    summaries = []  # 辟谣摘要
    sources = []  # 辟谣来源
    check_status = []  # 审核状态
    types = []  # 分类
    areas = []  # 地域
    third_parts = []  # 第三方标识
    remarks = []  # 备注
    texts = []  # 辟谣内容
    count = 1
    urls = get_ulrs()
    for url in urls:
        print(count, "访问...")
        tmp_url = "http://10.125.9.199:8080" + url
        html = get_html(tmp_url, headers=headers)
        count += 1
        if html == None:
            print("无效访问" + url)
        else:
            doc = pq(html)
            rumor_detail = doc.find("#inputForm")
            rumor_content = doc.find("#contentForm")
            text = rumor_content.find("td").text()
            rows = rumor_detail.find("tr")
            rows = [row for row in rows.items()]

            title = [td for td in rows[0].find("td").items()][1].text()
            tag = [td for td in rows[1].find("td").items()][1].text()
            summary = [td for td in rows[2].find("td").items()][1].text()
            src = [td for td in rows[3].find("td").items()][1].text()
            link = [td for td in rows[4].find("td").items()][1].text()
            check = [td for td in rows[5].find("td").items()][1].text()
            type = [td for td in rows[6].find("td").items()][1].text()
            area = [td for td in rows[7].find("td").items()][1].text()
            third_part = [td for td in rows[8].find("td").items()][1].text()
            remark = [td for td in rows[9].find("td").items()][1].text()
            titles.append(title)
            tags.append(tag)
            summaries.append(summary)
            sources.append(src)
            links.append(link)
            check_status.append(check)
            types.append(type)
            areas.append(area)
            third_parts.append(third_part)
            remarks.append(remark)
            texts.append(text)

    writer = pd.ExcelWriter(out_file, engine="xlsxwriter", options={'strings_to_urls': False})
    data = pd.DataFrame(
                {'辟谣主题': titles, "辟谣内容": texts, "辟谣信息标签": tags, "辟谣信息摘要": summaries,
                 "数据来源": sources, "原始链接地址": links, "审核状态": check_status, "分类": types,
                 "地域": areas, "第三方标识": third_parts, "备注": remarks
                 })
    data.to_excel(writer, index=False)
    writer.save()
