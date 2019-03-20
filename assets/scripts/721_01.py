import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.axisartist as axisartist

from matplotlib.transforms import Affine2D

fig = plt.figure(figsize = (10, 10))

ax = axisartist.Subplot(fig, 111)
ax.axis[:].set_visible(False)

ax.axis["x"] = ax.new_floating_axis(0,0)
ax.axis["x"].set_axisline_style("->", size = 1.0)
ax.axis["x"].label.set_text("$x_1$")

ax.axis["y"] = ax.new_floating_axis(1,0)
ax.axis["y"].set_axisline_style("->", size = 1.0)
ax.axis["y"].label.set_text("$x_2$")

ax.axis["x"].set_axis_direction("top")
ax.axis["y"].set_axis_direction("right")

ax.annotate("$y_1$", xy=(5, 5), xytext=(-5, -5),arrowprops=dict(arrowstyle="->"))
ax.annotate("$y_2$", xy=(-5, 5), xytext=(5, -5),arrowprops=dict(arrowstyle="->"))

x = np.random.uniform(-6, 6, 200)
y = x + np.random.uniform(-3, 3, 200)
ax.scatter(x, y)

fig.add_axes(ax)

plt.xlim(-5, 5)
plt.ylim(-5, 5)

plt.show()
# plt.tight_layout()
# plt.savefig('../images/721_01.png', transparent = True, bbox_inches = 'tight', pad_inches = 0.25) 