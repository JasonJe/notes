import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

tips = sns.load_dataset("tips")
anscombe = sns.load_dataset("anscombe")

fig = plt.figure(figsize=(12, 12))
sns.set_style('darkgrid')

plt.rcParams['font.sans-serif'] = ['SimHei'] # 设置显示中文
plt.rcParams['axes.unicode_minus'] = False # 正常显示坐标轴的负号

plt.subplot(3, 2, 1)
sns.regplot(x = "total_bill", y = "tip", data = tips) # 绘制回归直线和 95% 置信区间

plt.subplot(3, 2, 2)
plt.text(1, 9, u'regplot()对分类模型适应不好', fontdict = {'size': 12, 'color': 'r'})
sns.regplot(x = "size", y = "tip", data = tips)

plt.subplot(3, 2, 3)
sns.regplot(x = "x", y = "y", data = anscombe.query("dataset == 'II'"), ci = None) # 默认 1 阶模型进行拟合

plt.subplot(3, 2, 4)
sns.regplot(x = "x", y = "y", data = anscombe.query("dataset == 'II'"), ci = None, order = 2) # order = 2 使用 2 阶模型进行拟合

plt.subplot(3, 2, 5)
sns.regplot(x = "x", y = "y", data = anscombe.query("dataset == 'III'"), ci = None)

plt.subplot(3, 2, 6)
sns.regplot(x = "x", y = "y", data = anscombe.query("dataset == 'III'"), ci = None, robust = True) # 数据中有明显错误的数据点可以进行删除

plt.savefig('../images/752_07.png')
plt.show()