import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

sns.set_style('darkgrid')

fmri = sns.load_dataset("fmri")
sns.relplot(x = "timepoint", y = "signal", hue = "event", style = "event", kind = "line", sort = True, estimator = np.median, data = fmri)
# sort = True 选择对 x 进行排序
# estimator = np.median(np.max, np.min)为了使得线型更加平滑使用的聚合功能，表示对 x 变量的相同值进行多次测量，取平均，并取可信区间

plt.savefig('../images/752_06.png')
plt.show()