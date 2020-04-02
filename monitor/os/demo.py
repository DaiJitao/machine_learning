import psutil
from psutil import cpu_percent
import json
import os
import time
import pandas as pd


def mkdir(path):
    """
    创建目录
    """
    try:
        if not os.path.exists(path):
            os.makedirs(path)
            print("创建路径" + path + "成功！")
    except Exception as e:
        print("路径" + path + " 创建失败！")
        raise Exception(e)


one_G = 1073741824


def all_index(file=None):
    # 内存
    memory = psutil.virtual_memory()
    # 内存总量
    mem_total = memory.total / one_G
    mem_percent = memory.percent  # 内存使用率
    # 物理已使用的内存
    mem_used = memory.used / one_G
    # 可用内存
    mem_available = memory.available / one_G
    # cpu每秒使用率
    cpu_percen_interval = cpu_percent(interval=1)
    # 时间
    time_this = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    r_dict = {"time": [time_this], "mem_total": [mem_total], "mem_percent": [mem_percent],
              "cpu_percen_interval": [cpu_percen_interval], "mem_used": [mem_used], "mem_available": [mem_available]}
    df = pd.DataFrame(r_dict)
    if file:
        df.to_csv(file, mode='a', header=False)
        print("文件以保存" + file)
    else:
        file = "os.csv"
        df.to_csv(file, mode='a', header=False, index=False)
        print("文件以保存" + file)



if __name__ == '__main__':
    path = mkdir("F:/data")
    all_index()
