import random
import matplotlib.pyplot as plt

x = list(range(1, 11))
y = [random.randrange(1, 20) for i in range(1, 11)]

x2 = list(range(1, 11))
y2 = [random.randrange(1, 10) for i in range(1, 11)]

plt.plot(x, y, label='First Line') # 为线条指定名称
plt.plot(x2, y2, label='Second Line')

plt.xlabel('Plot Number') # X轴标签
plt.ylabel('Important var') # Y轴标签
plt.title('Line') # 标题
plt.legend() # 生成默认图例
plt.savefig('../images/751_01.png')
plt.show()
