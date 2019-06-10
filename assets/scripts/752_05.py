import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

sns.set_style('darkgrid')

tips = sns.load_dataset("tips")
sns.relplot(x = "total_bill", y = "tip", hue = "smoker", style = "smoker", data = tips) # 第 3 维的数据 smoker 列的数据用 hue="smoker" 和 style = "smoker" 用不同颜色和样式表示该维数据

plt.savefig('../images/752_05.png')
plt.show()