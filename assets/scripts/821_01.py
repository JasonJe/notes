import matplotlib.pyplot as plt
import numpy as np
import scipy

fig = plt.figure(figsize=(16, 8))
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

x = np.linspace(-5, 5)
y1 = 1/(1 + np.exp(- x))
y2 = np.exp(- x)/(1 + np.exp(- x))**2

plt.subplot(1, 2, 1)
plt.xlabel('x')
plt.ylabel('F(x)')
plt.title(u'$Logistic$ 分布函数')
plt.plot(x, y1, linewidth = 2.0)

plt.subplot(1, 2, 2)
plt.xlabel('x')
plt.ylabel('f(x)')
plt.title(u'$Logistic$ 密度函数')
plt.plot(x, y2, linewidth = 2.0)

plt.savefig('../images/821_01.png')
plt.show()