

from threading import Thread
import schedule
import psutil
from psutil import cpu_percent
import json
import os
import time
import pandas as pd
import socket

one_G = 1073741824

hostname=socket.gethostname()

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
              "cpu_percen_interval": [cpu_percen_interval], "mem_used": [mem_used], "mem_available": [mem_available],
              "hostname":hostname}
    df = pd.DataFrame(r_dict)
    print(r_dict)
    if file:
        df.to_csv(file, mode='a', header=False)
        print("文件以保存" + file)
    else:
        file = "os.csv"
        df.to_csv(file, mode='a', header=False, index=False,encoding='utf-8')
        print("文件以保存" + file)


def warning_task():
    t = Thread(target=all_index)
    t.start()


def main():
    time = 10
    schedule.every(time).minutes.do(warning_task)
    while True:
        schedule.run_pending()


if __name__ == '__main__':
    main()
