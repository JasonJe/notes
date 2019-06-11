import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

tips = sns.load_dataset("tips")
titanic = sns.load_dataset("titanic")

fig, ax = plt.subplots(3, 4, figsize=(16, 12))
sns.set_style('darkgrid')

plt.rcParams['font.sans-serif'] = ['SimHei'] # 设置显示中文
plt.rcParams['axes.unicode_minus'] = False # 正常显示坐标轴的负号

ax[0][0].set_title(u'分类散点图1(存在微小抖动)')
sns.catplot(x="day", y="total_bill", data=tips, ax=ax[0][0])

ax[0][1].set_title(u'分类散点图2(jitter = False来控制抖动大小)')
sns.catplot(x="day", y="total_bill", jitter = False,data=tips, ax=ax[0][1])

ax[0][2].set_title(u'分类散点图3(kind = "swarm"使得图形分布均匀)')
sns.catplot(x="day", y="total_bill", kind="swarm", data=tips, ax=ax[0][2])

ax[0][3].set_title(u'分类散点图4(增加第三维度)')
sns.catplot(x="day", y="total_bill", hue="sex", kind="swarm", data=tips, ax=ax[0][3])

ax[1][0].set_title(u'箱线图1')
sns.catplot(x="day", y="total_bill", kind="box", data=tips, ax=ax[1][0])

ax[1][1].set_title(u'箱线图2(增加第三维度)')
sns.catplot(x="day", y="total_bill", hue="smoker", kind="box", data=tips, ax=ax[1][1])

ax[1][2].set_title(u'小提琴图1(密度图和箱型图的结合)')
sns.catplot(x="day", y="total_bill", hue="time",kind="violin", data=tips, ax=ax[1][2])

ax[1][3].set_title(u'小提琴图2(增加第三维度，split = True 拆分小提琴)')
sns.catplot(x="day", y="total_bill", hue="sex",kind="violin", split=True, data=tips, ax=ax[1][3])

ax[2][0].set_title(u'条形图1(画出每个类别的平均值，黑色表示估计区间)')
sns.catplot(x="sex", y="survived", hue="class", kind="bar", data=titanic, ax=ax[2][0])

ax[2][1].set_title(u'条形图2(统计类别数量)')
sns.catplot(x="deck", kind="count", data=titanic, ax=ax[2][1])

ax[2][2].set_title(u'点图1(只画出估计值和区间)')
sns.catplot(x="sex", y="survived", hue="class", kind="point", data=titanic, ax=ax[2][2])

ax[2][3].set_title(u'点图2')
sns.catplot(x="class", y="survived", hue="sex",
            palette={"male": "g", "female": "m"},
            markers=["^", "o"], linestyles=["-", "--"],
            kind="point", data=titanic, ax=ax[2][3])

# fig.suptitle('标题', fontsize=20)
fig.tight_layout()
fig.savefig('../images/752_08.png')