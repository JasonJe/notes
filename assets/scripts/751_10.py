import random
import matplotlib.pyplot as plt

fig = plt.figure()
x = list(range(1, 11))
y = [random.randrange(1, 20) for i in range(1, 11)]

#### 绘制大图区域
left, bottom, width, height = 0.1, 0.1, 0.8, 0.8
ax1 = fig.add_axes([left, bottom, width, height]) # 确定大图左下角的位置以及宽高
ax1.plot(x, y, 'r')
ax1.set_xlabel('x')
ax1.set_ylabel('y')
ax1.set_title('title')

#### 绘制左上角的小图
ax2 = fig.add_axes([0.2, 0.6, 0.25, 0.25])
ax2.plot(x, y, 'b')
ax2.set_xlabel('x')
ax2.set_ylabel('y')
ax2.set_title('title inside 1')

#### 绘制右下角的小图，直接往plt里添加新的坐标系
plt.axes([0.6, 0.2, 0.25, 0.25])
plt.plot(y[::-1], x, 'g')
plt.xlabel('x')
plt.ylabel('y')
plt.title('title inside 2')
plt.savefig('../images/751_10.png')
plt.show()