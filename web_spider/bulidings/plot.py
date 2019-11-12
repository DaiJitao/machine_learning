import matplotlib.pyplot as plt

import pandas as pd
import matplotlib as mpl
mpl.rcParams['font.sans-serif'] = [u'SimHei']  # 黑体 FangSong/KaiTi
mpl.rcParams['axes.unicode_minus'] = False


d = pd.read_csv(r"F:\pycharm_workspce\dai_github\myproject\machine_learning\web_spider\bulidings\test1.csv", encoding='utf-8')
print(d)
plt.plot(d["月份"], d["房价（均价）"])
plt.grid(True)
plt.xticks(d["月份"])
plt.show()