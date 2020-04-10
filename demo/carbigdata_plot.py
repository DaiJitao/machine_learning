import pandas as pd
import matplotlib.pyplot as plt
import datetime
from pandas import DataFrame
import matplotlib.dates as mdate
import matplotlib

matplotlib.rcParams['font.family'] = ' STSong'  # 华文宋体
matplotlib.rcParams['font.size'] = 12  # 字体大小：20


def to_str(x):
    x = x.replace("-", "")
    return str(x).strip()


def sub_str(x):
    x = x.split(" ")
    return x[1]


def main(name, time, file):
    data_df = DataFrame()
    df = pd.read_csv(file)
    data_df = df.loc[:, ['time', 'mem_use_rate', 'cpu_use_rate']]
    data_df['time'] = data_df['time'].apply(to_str)
    mean_mem = data_df['mem_use_rate'].mean()
    mean_cpu = data_df['cpu_use_rate'].mean()
    # print(name[:6] + "内存使用率 " + str(mean_mem))
    print(name[:6] + "CPU使用率 " + str(mean_cpu))
    data_df = data_df.loc[data_df['time'].str.contains(time), :]
    time = data_df['time'].apply(sub_str)
    mem_use_rate = data_df['mem_use_rate']
    cpu_use_rate = data_df['cpu_use_rate']

    fig = plt.figure()
    fig.add_subplot(1, 1, 1)
    # ax.xaxis.set_major_formatter(mdate.DateFormatter('%Y-%m-%d %H:%M:%s'))  # 设置时间标签显示格式
    r = list(range(len(time)))[::3]
    xticks = time[::3]
    plt.plot(range(len(mem_use_rate)), mem_use_rate, label="内存使用率")
    plt.plot(range(len(mem_use_rate)), cpu_use_rate, "-.", label="CPU使用率")
    plt.axhline(mean_mem, color='r', linestyle='-', label="平均内存使用率(均值为" + str(mean_mem)[:4] + "%)")
    plt.axhline(mean_cpu, color="g", ls='-', marker='D', label="平均CPU使用率(均值为" + str(mean_cpu)[:4] + "%)")
    plt.legend()
    plt.grid(ls='-.')
    plt.xlabel("时间")
    plt.ylabel("百分比（%）")
    plt.title(name + "使用情况统计")
    plt.xticks(r, xticks, rotation=45)
    # plt.show()


if __name__ == '__main__':
    nums = ['3', '4', '5']
    num = nums[0]
    name_sers = [str(i) for i in range(194, 202)]
    for name_ser in name_sers:
        name = name_ser + "服务器 2020年4月" + num + "号"
        file = "F://data//os//" + name_ser + "os.csv"
        main(name=name, time='2020040' + num, file=file)
