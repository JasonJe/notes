import random
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

fig = plt.figure(figsize=(9, 16))

def create_plots():
    xs = []
    ys = []

    for x in range(10):
        y = random.randrange(10)
        xs.append(x)
        ys.append(y)
    return xs, ys

plt.subplot(10, 2, 1)
plt.plot(*create_plots())

plt.subplot(10, 2, 2)
plt.plot(*create_plots())

plt.subplot(10, 2, 3)
plt.plot(*create_plots())

plt.subplot(10, 2, 4)
plt.plot(*create_plots())

#### 
plt.subplot(10, 1, 3)
plt.plot(*create_plots())

plt.subplot(10, 3, 10)
plt.plot(*create_plots())

plt.subplot(10, 3, 11)
plt.plot(*create_plots())

plt.subplot(10, 3, 12)
plt.plot(*create_plots())

####
ax1 = plt.subplot2grid((10, 3), (4, 0), colspan=3)
ax1.plot([1, 2], [1, 2])
ax1.set_title('ax1_title')
ax2 = plt.subplot2grid((10, 3), (5, 0), colspan=2)
ax3 = plt.subplot2grid((10, 3), (5, 2), rowspan=2)
ax4 = plt.subplot2grid((10, 3), (6, 0))
ax4.scatter([1, 2], [2, 2])
ax4.set_xlabel('ax4_x')
ax4.set_ylabel('ax4_y')
ax5 = plt.subplot2grid((10, 3), (6, 1))

####
gs = gridspec.GridSpec(10, 3)
ax6 = plt.subplot(gs[7, :])
ax7 = plt.subplot(gs[8, :2])
ax8 = plt.subplot(gs[8:, 2])
ax9 = plt.subplot(gs[-1, 0])
ax10 = plt.subplot(gs[-1, -2])

plt.savefig('../images/751_09.png')
plt.show()