import matplotlib.pyplot as plt

slices = [7,2,2,13]
activities = ['sleeping','eating','working','playing']
cols = ['#d091da', '#6477f0', '#264fc9', '#117510']

plt.pie(slices,
        labels=activities,
        colors=cols,
        startangle=130,
        shadow= True,
        explode=(0,0.1,0,0),
        autopct='%1.1f%%')

plt.title('Pie')
plt.savefig('../images/751_04.png')
plt.show()