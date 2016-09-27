import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

style.use('seaborn-darkgrid')

fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)


def animate(i):
    with open("values.txt", "r") as rvalues_file:
        graph_data = rvalues_file.read()
    lines = graph_data.split('\n')
    xar = []
    yar = []
    for line in lines:
        if len(line) > 1:
            x, y = line.split(',')
            xar.append(float(x))
            yar.append(float(y))
    ax1.clear()
    ax1.plot(xar, yar)

ani = animation.FuncAnimation(fig, animate)
plt.show()
