import itchat


# 登入并保存登入状态，实现第一次运行时扫码，一定时间内再次运行就不用扫码了，手机微信上将显示：网页微信已登入.....
itchat.auto_login(hotReload=True)
# 发送文本数据到文件助手
itchat.send("东小东你好123", toUserName="filehelper")
