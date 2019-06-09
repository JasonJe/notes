import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

x = np.random.randn(200)

fig = plt.figure(figsize=(14, 5))
sns.set_style('darkgrid')

plt.subplot(1, 2, 1)
sns.distplot(x) # 单变量分布

plt.subplot(1, 2, 2)
sns.distplot(x, hist = False) # 取消直方图显示

plt.savefig('../images/752_02.png')
plt.show()