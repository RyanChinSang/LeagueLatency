import sys
import subprocess
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import itertools
from matplotlib import style, text
from datetime import datetime
from matplotlib.widgets import RadioButtons


style.use('fivethirtyeight')
np.seterr(invalid='ignore')
ltimes = []
lpings = []
avg = 0
count = 0
sum_ping = 0
min_ping = float('+inf')
max_ping = float('-inf')
count_na = 0
sum_ping_na = 0
min_ping_na = float('+inf')
max_ping_na = float('-inf')
count_lan = 0
sum_ping_lan = 0
min_ping_lan = float('+inf')
max_ping_lan = float('-inf')
start = datetime.now()
fig = plt.figure(figsize=(16, 9))
ax1 = fig.add_subplot(1, 1, 1)
servers = {"NA": "104.160.131.3", "LAN": "104.160.136.3"}
rax = plt.axes([0.874, 0.892, 0.089, 0.089], aspect='equal', frameon=True, axisbg='white')
radio = RadioButtons(rax, servers.keys())
radio_value = radio.value_selected


def handle_close(event):
    sys.exit()


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
        if len(data1) > 1:
            if index == 0:
                data1[index + 1] = data2[index + 1]
            elif index == len(data2) - 1:
                data1[index - 1] = data2[index - 1]
            else:
                data1[index - 1] = data2[index - 1]
                data1[index + 1] = data2[index + 1]
        else:
            pass


def upd_data():
    global lpings, ltimes, sum_ping, count, max_ping, min_ping, radio_value, servers
    global sum_ping_na, count_na, max_ping_na, min_ping_na
    global sum_ping_lan, count_lan, max_ping_lan, min_ping_lan
    p1 = subprocess.Popen(["ping.exe", servers[radio_value], "-n", "1", "-l", "500"],
                          stdout=subprocess.PIPE,
                          stdin=subprocess.PIPE,
                          stderr=subprocess.PIPE,
                          shell=False)
    while p1.poll() is None:
        line = p1.stdout.readline()
        if "time=" in line:
            ping = float(line[line.find("time=")+5:line.find("ms")])
            if radio_value == "NA":
                sum_ping_na += ping
                count_na += 1
                if ping > max_ping_na:
                    max_ping_na = ping
                if min_ping_na > ping:
                    min_ping_na = ping
            if radio_value == "LAN":
                sum_ping_lan += ping
                count_lan += 1
                if ping > max_ping_lan:
                    max_ping_lan = ping
                if min_ping_lan > ping:
                    min_ping_lan = ping
            lpings += [ping]
            interval = datetime.now() - start
            ltime = interval.total_seconds()
            ltimes += [ltime]
    radio_value = radio.value_selected


def animate(i):
    global max_ping, min_ping, sum_ping, ltimes, lpings, count, radio_value, servers, avg
    global sum_ping_na, count_na, max_ping_na, min_ping_na
    global sum_ping_lan, count_lan, max_ping_lan, min_ping_lan

    nppings = np.array(lpings)
    nptimes = np.array(ltimes)

    gpings = nppings.copy()
    ypings = nppings.copy()
    rpings = nppings.copy()

    gpings[gpings >= 200] = np.nan

    ypings[ypings < 200] = 0
    ypings[ypings >= 500] = 0
    ypings[ypings == 0] = np.nan
    link(ypings, nppings)

    rpings[rpings < 500] = np.nan
    link(rpings, nppings)

    if radio_value == "NA":
        if count_na < 1:
            avg = sum_ping_na
        else:
            avg = sum_ping_na / count_na
        max_ping = max_ping_na
        min_ping = min_ping_na
    if radio_value == "LAN":
        if count_lan < 1:
            avg = sum_ping_lan
        else:
            avg = sum_ping_lan / count_lan
        max_ping = max_ping_lan
        min_ping = min_ping_lan
    ax1.clear()
    ax1.text(0.925, 1.025, 'by Ryan Chin Sang', ha='right', va='top', transform=ax1.transAxes, color='0.85', size='small')
    ax1.set_ylabel('Ping /ms')
    ax1.set_xlabel('Time /s')
    ax1.set_title('Ping to League of Legends [' + radio_value + '] Server (' + servers[radio_value] + ')')

    ax1.plot(nptimes, gpings, linewidth=1.5, color='g')
    ax1.plot(nptimes, ypings, linewidth=1.5, color='y')
    ax1.plot(nptimes, rpings, linewidth=1.5, color='r')

    upd_data()


def animate2():
    fig.canvas.mpl_connect('close_event', handle_close)
    fig.canvas.set_window_title('LoLPing v1.9a')
    ani = animation.FuncAnimation(fig, animate, frames=60)
    plt.show()

upd_data()
animate2()
