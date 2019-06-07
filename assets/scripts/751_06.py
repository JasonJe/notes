import numpy as np
import matplotlib.pyplot as plt

def f(x,y): # 高度函数
    return (1 - x / 2 + x**5 + y**3) * np.exp(-x**2 -y**2)

n = 256
x = np.linspace(-3, 3, n)
y = np.linspace(-3, 3, n)
X,Y = np.meshgrid(x, y)

plt.contourf(X, Y, f(X, Y), 8, alpha=.75, cmap = plt.cm.hot) # 进行颜色填充

C = plt.contour(X, Y, f(X, Y), 8, colors='black', linewidth = 0.5) 

plt.clabel(C, inline=True, fontsize=10) # 添加高度数字

# 隐藏坐标轴
plt.xticks(())
plt.yticks(())
plt.title('Contour')

plt.savefig('../images/751_06.png')
plt.show()