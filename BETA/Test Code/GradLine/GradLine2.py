import matplotlib.pyplot as plt
import numpy as np
import matplotlib.collections as mcoll
import matplotlib.path as mpath
from matplotlib.colors import LinearSegmentedColormap

colors = [(0, 1, 0), (1, 1, 0), (1, 0, 0)]
cmap_name = 'gyr'

def colorline(x,
              y,
              z=None,
              cmap=LinearSegmentedColormap.from_list(cmap_name, colors),
              norm=plt.Normalize(0.0, 1.0),
              linewidth=2,
              alpha=1.0):
    """
    http://nbviewer.ipython.org/github/dpsanders/matplotlib-examples/blob/master/colorline.ipynb
    http://matplotlib.org/examples/pylab_examples/multicolored_line.html
    Plot a colored line with coordinates x and y
    Optionally specify colors in the array z
    Optionally specify a colormap, a norm function and a line width
    """

    # Default colors equally spaced on [0,1]:
    if z is None:
        z = np.linspace(0.0, 1.0, len(x))

    # Special case if a single number:
    if not hasattr(z, "__iter__"):  # to check for numerical input -- this is a hack
        z = np.array([z])

    z = np.asarray(z)

    segments = make_segments(x, y)
    lc = mcoll.LineCollection(segments, array=z, cmap=cmap, norm=norm, linewidth=linewidth, alpha=alpha)
    # lc = mcoll.LineCollection(segments, array=z, cmap=cmap, linewidth=linewidth, alpha=alpha)

    ax = plt.gca()
    ax.add_collection(lc)
    ax.set_xlim([0, x.max()])
    ax.set_ylim([y.min(), y.max()])

    return lc


def make_segments(x, y):
    """
    Create list of line segments from x and y coordinates, in the correct format
    for LineCollection: an array of the form numlines x (points per line) x 2 (x
    and y) array
    """

    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    print segments
    return segments

# N = 10
# np.random.seed(101)
# x = np.random.rand(N)
# y = np.random.rand(N)

times = [0.311, 0.761, 1.148, 1.533, 1.928, 2.329, 2.719, 3.108, 3.493, 3.903, 4.318, 4.703, 5.108, 5.507, 5.913, 6.321, 6.726, 7.133, 7.523, 7.934, 8.346, 8.742, 9.154, 9.548, 9.953, 10.353, 10.758, 11.147, 11.543, 11.943, 12.353]
pings = [122.0, 118.0, 118.0, 117.0, 120.0, 117.0, 117.0, 117.0, 118.0, 118.0, 119.0, 119.0, 120.0, 117.0, 120.0, 125.0, 119.0, 118.0, 120.0, 120.0, 132.0, 117.0, 119.0, 121.0, 117.0, 119.0, 120.0, 117.0, 121.0, 118.0, 122.0]
x = np.array(times)
y = np.array(pings)

# print x
# print y

fig, ax = plt.subplots()

path = mpath.Path(np.column_stack([x, y]))
verts = path.interpolated(steps=3).vertices
x, y = verts[:, 0], verts[:, 1]
z = np.linspace(0, 1, len(x))
# z = np.linspace(0, 100, len(x))
# colorline(x, y, z, cmap=plt.get_cmap('jet'), linewidth=2)
# colorline(x, y, z, cmap=LinearSegmentedColormap.from_list(cmap_name, colors), linewidth=2)
colorline(x, y, z)

plt.show()

# make segments be the length of a delay 200<=ping<=499 is yellow and ping>499 is red
# set up dummy data array and plot with that
