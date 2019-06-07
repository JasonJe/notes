import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 5 * np.pi, 1000)
y = np.sin(x)
y2 = np.sin(2 * x)

fig = plt.figure() # 创建一个图像窗口
ax = plt.subplot2grid((1, 1), (0, 0)) # 创建 1 个小图，整个图像窗口分成 1 行 1 列

ax.plot(x, y, label='First Line')
ax.plot(x, y2, label='Second Line')

# 填充
ax.fill(x, y, color = "g", alpha = 0.3) # 对函数与坐标轴之间的区域进行填充
ax.fill_between(x, y, y2, facecolor = "b", alpha = 0.5) # 填充两个函数之间的区域

# 坐标轴设置相关
ax.grid(True, color='g', linestyle='--', linewidth = 1)
ax.xaxis.label.set_color('c') # 设置 x 轴标签颜色
ax.yaxis.label.set_color('r') # 设置 y 轴标签颜色
ax.set_yticks([-1, 0, 1]) # 设置 y 轴刻度与范围

# 注释和标记相关
x0 = np.pi / 2
y0 = np.sin(x0)
plt.annotate(r'$sin(x)$', xy=(x0, y0), xycoords='data', xytext=(+30, -30), textcoords='offset points', fontsize=12, arrowprops=dict(arrowstyle='->', connectionstyle="arc3,rad=.2")) # xycoords='data' 基于数据的值来选位置, xytext = (+30, -30) xy 偏差值，textcoords='offset points' 对于标注位置的描述，arrowprops 箭头类型设置
plt.text(0, -1.1, r'$Some\ text.$', fontdict={'size': 12, 'color': 'r'}) # 0, -1.1 选取text的位置

plt.xlabel('X')
plt.ylabel('Y')
plt.title('Style')
plt.legend(loc = 'upper left')
plt.savefig('../images/751_08.png')
plt.show()