import requests


sess = requests.Session()

response = sess.get("http://www.baidu.com")

print(sess.cookies)
print(response.text)
print("请求头",response.request.headers)
print()
print("响应头",response.headers)

sess.close()

