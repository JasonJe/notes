import random
import matplotlib.pyplot as plt

x = list(range(1, 11))
y = [random.randrange(1, 20) for i in range(1, 11)]

plt.scatter(x,y, label='Scatter', color='k', s=25, marker="o")

plt.xlabel('x')
plt.ylabel('y')
plt.title('Scatter')
plt.legend()
plt.savefig('../images/751_03.png')
plt.show()