import matplotlib.pyplot as plt
import numpy as np

pingar = np.array([])


def arsize(data):
    return data.size - np.count_nonzero(np.isnan(data))


def armatch(data1, data2):
    i = 0
    for val in data1:
        i += 1
        if np.isnan(val):
            data2[i - 1] = np.nan


def rmv_dup(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


def link(data1, data2):
    """
    data1 and data2 must be lists of same datatype and of equal size
    link data1 to data2 for where there are matches in the values between data1 and data2
    ie. surround data1's values with values in data2
    """
    seen = set()
    seen_add = seen.add
    loc_list = []
    dloc_list = []
    for val1 in data2:
        for val2 in data1:
            if val2 == val1:
                for loc in np.where(data1 == val1)[0]:
                    loc_list += [loc]
                    dloc_list += [x for x in loc_list if not (x in seen or seen_add(x))]
    for index in dloc_list:
        if index == 0:
            data1[index + 1] = data2[index + 1]
        elif index == len(data2) - 1:
            data1[index - 1] = data2[index - 1]
        else:
            data1[index - 1] = data2[index - 1]
            data1[index + 1] = data2[index + 1]

times = [0.311, 0.761, 1.148, 1.533, 1.928, 2.329, 2.719, 3.108, 3.493, 3.903, 4.318, 4.703, 5.108, 5.507, 5.913, 6.321, 6.726, 7.133, 7.523, 7.934, 8.346, 8.742, 9.154, 9.548, 9.953, 10.353, 10.758, 11.147, 11.543, 11.943, 12.353, 12.753]
pings = [122.0, 118.0, 118.0, 117.0, 120.0, 117.0, 117.0, 117.0, 118.0, 118.0, 119.0, 119.0, 120.0, 117.0, 120.0, 125.0, 119.0, 118.0, 120.0, 120.0, 132.0, 117.0, 119.0, 121.0, 117.0, 119.0, 120.0, 117.0, 121.0, 118.0, 122.0, 121.0]
nptimes = np.array(times)
nppings = np.array(pings)
gpings = nppings.copy()
ypings = nppings.copy()
rpings = nppings.copy()

gpings[gpings > 120] = np.nan
# link(gpings, nppings)

ypings[ypings <= 120] = 0
ypings[ypings >= 124.0] = 0
ypings[ypings == 0] = np.nan
link(ypings, nppings)

rpings[rpings < 124] = np.nan
link(rpings, nppings)


rtpings = np.array([])
ytpings = np.array([])
gtpings = np.array([])

# for n in range(len(pings)):
for val in nppings:
    # if val > 500:
    if val > 124:
        rtpings = np.append(rtpings, [val])
        typings = np.append(ytpings, [np.nan])
        gtpings = np.append(gtpings, [np.nan])
    if val > 120:
        rtpings = np.append(rtpings, [np.nan])
        typings = np.append(ytpings, [val])
        gtpings = np.append(gtpings, [np.nan])
    else:
        rtpings = np.append(rtpings, [np.nan])
        typings = np.append(ytpings, [np.nan])
        gtpings = np.append(gtpings, [val])

# link(rtpings, nppings)
# link(ytpings, nppings)

print 'r'
print rpings
print rtpings
print 'y'
print ypings
print ytpings
print 'g'
print gpings
print gtpings

#plotting
plt.style.use('seaborn-darkgrid')
ax1 = plt.gca()
plt.plot(nptimes, gpings, color='g')
plt.plot(nptimes, ypings, color='y')
plt.plot(nptimes, rpings, color='r')
# print ax1.get_xlim(), ax1.get_ylim(),  nppings.min(), nppings.max()
# pingar = np.append(pingar, pings)
# print pingar
# pingar = np.append(pingar, [123.0])
# print pingar, str(pingar[-1])
# if nppings.max() >= 200
plt.fill_between(nptimes, 0, 200, facecolor='green', interpolate=True, alpha=0.05)
plt.fill_between(ax1.get_xlim(), 60, 120, facecolor='blue', interpolate=True, alpha=0.05)
plt.fill_between(nptimes, 200, 500, facecolor='yellow', interpolate=True, alpha=0.05)
plt.fill_between(nptimes, 500, 900, facecolor='red', interpolate=True, alpha=0.05)
plt.show()
