import re



res = "保存到相册20198172211上传来自山水句容手机客户端"

res = re.sub(r"([a-zA-Z\d]){8,}", "", res) # 8个字符以上的英文 ([^\u4e00-\u9fa5a-zA-Z\d])
res = re.sub(r"([^\u4e00-\u9fa5a-zA-Z\d])", "", res) # 去除特殊符号

print(res)