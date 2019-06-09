import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

mean, cov = [0, 1], [(1, .5), (.5, 1)]
data = np.random.multivariate_normal(mean, cov, 200)
df = pd.DataFrame(data, columns=["x", "y"])

sns.set_style('darkgrid')

sns.jointplot(x="x", y="y", data=df)
# sns.jointplot(x="x", y="y", data=df, kind="kde") # 指定绘制的图像类型，scatter, reg, resid, kde, hex

plt.savefig('../images/752_03.png')
plt.show()