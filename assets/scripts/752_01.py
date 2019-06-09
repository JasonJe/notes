import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

def sinplot(flip=1):
    x = np.linspace(0, 14, 100)
    for i in range(1, 7):
        plt.plot(x, np.sin(x + i * .5) * (7 - i) * flip)

# 对两种画图进行比较
fig = plt.figure()
sns.set() # sns.set_style('dark') 预设的主题，一共有五种，darkgrid，whitegrid，dark，white，和ticks
sinplot()
plt.savefig('../images/752_01.png')
plt.show()