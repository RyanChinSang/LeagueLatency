import matplotlib.pyplot as plt
import numpy as np

x = np.arange(0.0, 2, 0.01)
y1 = np.sin(2*np.pi*x)
y2 = 1.2*np.sin(4*np.pi*x)

# fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)

# ax1.fill_between(x, 0, y1)
# ax1.set_ylabel('between y1 and 0')

# ax2.fill_between(x, y1, 1)
# ax2.set_ylabel('between y1 and 1')
#
# ax3.fill_between(x, y1, y2)
# ax3.set_ylabel('between y1 and y2')
# ax3.set_xlabel('x')

# now fill between y1 and y2 where a logical condition is met.  Note
# this is different than calling
#   fill_between(x[where], y1[where],y2[where]
# because of edge effects over multiple contiguous regions.

# fig, (ax, ax1) = plt.subplots(2, 1, sharex=True)
# ax.plot(x, y1, x, y2, color='black')
# ax.fill_between(x, y1, y2, where=y2 >= y1, facecolor='green', interpolate=True)
# ax.fill_between(x, y1, y2, where=y2 <= y1, facecolor='red', interpolate=True)
# ax.set_title('fill between where')

# Test support for masked arrays.
# y2 = np.ma.masked_greater(y2, 1.0)

# ax1.plot(x, y1, x, y2, color='black')
# ax1.fill_between(x, y1, y2, where=y2 >= y1, facecolor='green', interpolate=True)
# ax1.fill_between(x, y1, y2, where=y2 <= y1, facecolor='red', interpolate=True)
# ax1.set_title('Now regions with y2>1 are masked')

# This example illustrates a problem; because of the data
# gridding, there are undesired unfilled triangles at the crossover
# points.  A brute-force solution would be to interpolate all
# arrays to a very fine grid before plotting.

# show how to use transforms to create axes spans where a certain condition is satisfied
fig, ax = plt.subplots()
y = 1000*np.sin(4*np.pi*x)
ax.plot(x, y, color='black')

# use the data coordinates for the x-axis and the axes coordinates for the y-axis
import matplotlib.transforms as mtransforms
trans = mtransforms.blended_transform_factory(ax.transData, ax.transAxes)
theta = 0.9
lim = float(ax.get_xbound()[0])
# print ax.get_xbound(), ax.get_ybound()
# print ax.get_xlim(), ax.get_ylim()
# print y.max(), x.max()
# ax.axhline(theta, color='green', lw=2, alpha=0.5)
# ax.axhline(-theta, color='red', lw=2, alpha=0.5)
# ax.fill_between(x, 0, 1, where=y > theta, facecolor='green', alpha=0.5, transform=trans)
# ax.fill_between(x, 0, 1, where=y < -theta, facecolor='red', alpha=0.5, transform=trans)

# ax.fill_between(x, ax.get_ylim()[0], ax.get_ylim()[1], where=y > float('-inf'), facecolor='red', alpha=0.5, transform=trans)

# ax.fill_between(ax.get_xlim(), ax.get_ylim()[0], ax.get_ylim()[1], facecolor='red', alpha=0.5, transform=trans)
# ax.fill_between(ax.get_xbound(), ax.get_ybound()[0], ax.get_ybound()[1], facecolor='blue', alpha=0.5)

# ax.axhspan(ax.get_ylim()[0], ax.get_ylim()[1], color='green')
# ax.axvspan(ax.get_xlim()[0], ax.get_xlim()[1], color='green')

# ax.axvspan(ax.get_xbound()[0], ax.get_xbound()[1], color='green')
# ax.set_ylim((1.1*y.min(), 1.1*y.max()))
# ax.set_xlim((1.1*x.min(), 1.1*x.max()))

yax_min = 1.1*y.min()
yax_max = 1.1*y.max()

ax.set_ylim([yax_min, yax_max])

# xax_min = 1.1*x.min()
# xax_max = 1.1*x.max()

# print ax.get_xbound(), ax.get_ybound()
print ax.get_xlim(), ax.get_ylim(), y.min()
# print y.max(), x.max()

if yax_max > 500:
    ax.axhspan(yax_min, 200, fc='green', ec='none', alpha=0.25)
    ax.axhspan(200, 500, fc='yellow', ec='none', alpha=0.25)
    ax.axhspan(500, yax_max, fc='red', ec='none', alpha=0.25)
elif yax_max > 200:
    ax.axhspan(yax_min, 200, fc='green', ec='none', alpha=0.25)
    ax.axhspan(200, yax_max, fc='yellow', ec='none', alpha=0.25)
else:
    ax.axhspan(yax_min, yax_max, fc='green', ec='none', alpha=0.25)

# ax.axvspan(1.1*x.min(), 1.1*x.max(), color='green')

plt.show()