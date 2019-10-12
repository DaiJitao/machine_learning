import subprocess
import time

#
today = time.strftime("%Y-%m-%d %H:%M", time.localtime(time.time()))


def lines(file):
    try:
        with open(file, "r") as c:
            lines = c.readlines()
        return lines
    except:
        pass


def date_to_seconds(date, mode="%Y-%m-%d %H:%M:%S"):
    ''' 日期转化为秒 '''
    try:
        timeArray = time.strptime(date, mode)
        timeStamp = int(time.mktime(timeArray))  # 秒
        return timeStamp
    except Exception as e:
        print("解析异常", e)


def filter_file(files, intervaltime):
    res_file = []
    for line in files[1:]:
        file = line.strip().split(" ")
        day = file[-3].strip()
        timeH = file[-2].strip()
        date = day + " " + timeH
        timeStamp = date_to_seconds(date, mode="%Y-%m-%d %H:%M")
        todayStamp = date_to_seconds(today, mode="%Y-%m-%d %H:%M")
        if (todayStamp - timeStamp) >= intervaltime:
            filepath = file[-1].strip()
            res_file.append(filepath)

    return res_file


def delete(hdfspath, intervaltime, history_file):
    data = subprocess.getstatusoutput("hdfs dfs -ls " + hdfspath + "> " + history_file)
    if data[0] == 0:
        res = filter_file(files=lines(history_file), intervaltime=intervaltime)
        count = 0
        for file in res:
            print("开始删除文件:" + file)
            isDelete = subprocess.getstatusoutput("hdfs dfs -rm " + file)
            if isDelete[0] == 0:
                count += 1
                print("文件 " + file + " 删除成功")
            else:
                print("文件 " + file + " 删除失败")
        name = hdfspath.split("/")[1]
        print(name + "一共删除 " + str(count) + " 文件")
    else:
        print("获取文件列表命令失败")


def sentiment_file_delete(history_file):
    hdfspath = "/sentiment/tempDir/"
    intervaltime = int(0.25 * 24 * 60 * 60)  # 1/4天
    print("情感分析 临时目录开始检查文件...")
    delete(hdfspath, intervaltime, history_file)
    print("情感分析task目录开始检查文件...")
    hdfspath = "/sentiment/taskDir/"
    intervaltime = 1 * 24 * 60 * 60  # 1天
    delete(hdfspath, intervaltime, history_file)
    print("情感分析文件删除完毕")
    return True


def classify_delete(history_file):
    hdfspath = "/classify/tempDir/"
    intervaltime = 3 * 24 * 60 * 60  # 3天
    print("分类分析 临时目录开始检查文件...")
    delete(hdfspath, intervaltime, history_file)
    print("分类分析task目录开始检查文件...")
    hdfspath = "/classify/taskDir/"
    intervaltime = 7 * 24 * 60 * 60  # 3天
    delete(hdfspath, intervaltime, history_file)
    print("分类分析文件删除完毕")


def praise_delete(history_file):
    print("口碑分析 task目录开始检查文件...")
    hdfspath = "/publicPraise/taskDir"
    intervaltime = 7 * 24 * 60 * 60  # 3天
    delete(hdfspath, intervaltime, history_file)
    print("口碑分析文件删除完毕")


def newshottopic_delete(history_file):
    print("热点分析 task目录开始检查文件...")
    hdfspath = "/newshottopic/taskDir"
    intervaltime = 7 * 24 * 60 * 60  # 3天
    delete(hdfspath, intervaltime, history_file)
    print("热点分析文件删除完毕")


if __name__ == "__main__":
    history_file = "history_file.txt"
    isFlag = False  # 是否执行完
    while True:
        # 定时任务，20分钟执行一次
        one_hour = 20 * 60
        isFlag = sentiment_file_delete(history_file)
        time.sleep(one_hour)
        #  newshottopic_delete(history_file)
        # praise_delete(history_file)
        # classify_delete(history_file)
