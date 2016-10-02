import sys
import subprocess
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from datetime import datetime
from matplotlib.widgets import RadioButtons

CREATE_NO_WINDOW = 0x08000000
style.use('seaborn-darkgrid')
ltimes = []
lpings = []
avg_lis = []
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
icon_manager = matplotlib.pyplot.get_current_fig_manager()
icon_manager.window.wm_iconbitmap("icon.ico")
ax1 = fig.add_subplot(1, 1, 1)
servers = {"NA": "104.160.131.3", "LAN": "104.160.136.3"}
rax = plt.axes([0.881, 0.617, 0.089, 0.089], aspect='equal', frameon=True, axisbg='white')
radio = RadioButtons(rax, servers.keys())
radio_value = radio.value_selected


def handle_close(event):
    sys.exit()


def upd_data():
    global lpings, ltimes, sum_ping, count, max_ping, min_ping, radio_value, servers
    global sum_ping_na, count_na, max_ping_na, min_ping_na
    global sum_ping_lan, count_lan, max_ping_lan, min_ping_lan
    p1 = subprocess.Popen(["ping.exe", servers[radio_value], "-n", "1", "-l", "500"],
                          stdout=subprocess.PIPE,
                          stdin=subprocess.PIPE,
                          stderr=subprocess.PIPE,
                          shell=False,
                          creationflags=CREATE_NO_WINDOW)
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
    global max_ping, min_ping, sum_ping, ltimes, lpings, count, radio_value, servers, avg, avg_lis
    global sum_ping_na, count_na, max_ping_na, min_ping_na
    global sum_ping_lan, count_lan, max_ping_lan, min_ping_lan
    ping_val = str(lpings[count-1])
    time_val = str(ltimes[count-1])
    yar = lpings
    xar = ltimes
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
    avg_lis += [avg]
    ax1.clear()
    ax1.text(0.999, 1.02, 'by Ryan Chin Sang', ha='right', va='top', color='0.85', size='small', transform=ax1.transAxes)
    if (0.9 * avg) <= float(ping_val) <= (1.1 * avg):
        ax1.text(1.01, 0.973, "Ping: " + ping_val + " ms", transform=ax1.transAxes, linespacing=0.1,
                 bbox={'alpha': 0.23, 'pad': 5, "fc": "green", "lw": 2})
    elif float(ping_val) > (1.1 * avg):
        ax1.text(1.01, 0.973, "Ping: " + ping_val + " ms", transform=ax1.transAxes, linespacing=0.1,
                 bbox={'alpha': 0.3, 'pad': 5, "fc": "red", "lw": 2})
    else:
        ax1.text(1.01, 0.973, "Ping: " + ping_val + " ms", transform=ax1.transAxes, linespacing=0.1,
                 bbox={'alpha': 0.14, 'pad': 5, "fc": "blue", "lw": 2})
    if float(ping_val) < avg:
        ax1.text(1.01, 0.923, "Avg: " + format(avg, '.3f') + " ms", transform=ax1.transAxes, linespacing=0.1,
                 bbox={'alpha': 0.23, 'pad': 5, "fc": "green", "lw": 2})
    elif float(ping_val) > avg:
        ax1.text(1.01, 0.923, "Avg: " + format(avg, '.3f') + " ms", transform=ax1.transAxes, linespacing=0.1,
                 bbox={'alpha': 0.3, 'pad': 5, "fc": "red", "lw": 2})
    else:
        ax1.text(1.01, 0.923, "Avg: " + format(avg, '.3f') + " ms", transform=ax1.transAxes, linespacing=0.1,
                 bbox={'alpha': 0.14, 'pad': 5, "fc": "blue", "lw": 2})
    ax1.text(1.01, 0.873, "Time: " + time_val + " s", transform=ax1.transAxes, linespacing=0.1,
             bbox={'alpha': 0.14, 'pad': 5, "fc": "blue", "lw": 2})
    ax1.text(1.01, 0.823, "Max: " + str(max_ping) + " ms", transform=ax1.transAxes, linespacing=0.1,
             bbox={'alpha': 0.14, 'pad': 5, "fc": "blue", "lw": 2})
    ax1.text(1.01, 0.773, "Min: " + str(min_ping) + " ms", transform=ax1.transAxes, linespacing=0.1,
             bbox={'alpha': 0.14, 'pad': 5, "fc": "blue", "lw": 2})
    ax1.set_ylabel('Ping /ms')
    ax1.set_xlabel('Time /s')
    ax1.set_title('Ping to League of Legends [' + radio_value + '] Server (' + servers[radio_value] + ')')
    ax1.plot(xar, yar, linewidth=1.0)
    ax1.plot(xar, avg_lis, linewidth=0.5)
    upd_data()


def animate2():
    fig.canvas.mpl_connect('close_event', handle_close)
    fig.canvas.set_window_title('LoLPing v2.0a')
    ani = animation.FuncAnimation(fig, animate, frames=60)
    plt.show()

upd_data()
animate2()
