import random
import matplotlib.pyplot as plt

x = list(range(1, 11, 2))
y = [random.randrange(1, 20) for i in range(1, 6)]

x2 = list(range(2, 12, 2))
y2 = [random.randrange(1, 10) for i in range(1, 6)]

plt.bar(x, y, label="Example one")
plt.bar(x2, y2, label="Example two", color='g')

plt.xlabel('Bar Number')
plt.ylabel('Bar Height')
plt.title('Bar')
plt.legend()

plt.savefig('../images/751_02.png')
plt.show()


