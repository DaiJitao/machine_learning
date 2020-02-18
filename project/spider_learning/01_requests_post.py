import requests
from lxml import etree
#post
def demo_post(url):
    data = {}

    response = requests.post(url, data)


def get_all_proxy():
    #观察西刺代理的高匿页面翻页时候是每页从1往上加的一共3602页遍历页面
    for s in range(1,4029):
        url = "https://www.xicidaili.com/nn/" + str(s)
        print(url)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        }
        response = requests.get(url, headers=headers)
        #保存西刺代理页面xcdl.html
        with open('xcdl.html', 'wb') as f:
            f.write(response.content)

        html_ele = etree.HTML(response.text)
        #xpath拿到IP和端口路径
        ip_eles = html_ele.xpath('//tr/td[2]/text()')
        port_ele = html_ele.xpath('//tr/td[3]/text()')
        print(len(ip_eles))
        print(len(port_ele))
        #把IP和端口添加到列表里
        proxy_list = []
        for i in range(0,len(ip_eles)):
            proxy_str = 'http://' + ip_eles[i] + ':' + port_ele[i]
            proxy_list.append(proxy_str)

        return proxy_list
        # 利用访问百度测试IP有效性


def check_all_proxy(proxy_list):
    valid_proxy_list = []
    for proxy in proxy_list:
        url = 'http://www.baidu.com/s?wd=ip'
        proxy_dict = {
            'http': proxy
        }
        try:
            response = requests.get(url, proxies=proxy_dict, timeout=1)
            if response.status_code == 200:
                print('代理可用：' + proxy)
                valid_proxy_list.append(proxy)
            else:
                print('代理超时')
        except:
            pass
            print('代理不可用--------------->')
    return valid_proxy_list




def demo_proxy(url, isProxy):
    """
    https://www.xicidaili.com/?id=924
    :return:
    """
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36"}
    if isProxy:
        free_proxy = {"http":"/114.226.246.21:9999"}
        response = requests.get(url=url,headers=headers, proxies=free_proxy)
    else:
        response = requests.get(url,headers=headers)
    print(response.status_code)




if __name__ == '__main__':
    # demo_proxy("http://www.baidu.com", False)
    proxy_list  = get_all_proxy()
    valid_proxy_list = check_all_proxy(proxy_list)