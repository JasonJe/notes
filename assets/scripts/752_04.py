import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

sns.set_style('darkgrid')

iris = sns.load_dataset("iris")
sns.pairplot(iris);
# 对角线化的是单变量的分布

plt.savefig('../images/752_04.png')
plt.show()