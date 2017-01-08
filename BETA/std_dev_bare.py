import sys
import subprocess
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style, text
from datetime import datetime
from matplotlib.widgets import RadioButtons


style.use('fivethirtyeight')
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
    ax1.clear()
    ax1.text(0.925, 1.025, 'by Ryan Chin Sang', ha='right', va='top', transform=ax1.transAxes, color='0.85', size='small')
    ax1.set_ylabel('Ping /ms')
    ax1.set_xlabel('Time /s')
    ax1.set_title('Ping to League of Legends [' + radio_value + '] Server (' + servers[radio_value] + ')')
    ax1.plot(xar, yar, linewidth=1.5, label="Ping: " + ping_val + "ms     "
                                            + "Time: " + time_val + "s\n"
                                            + "Avg: " + format(avg, '.3f') + " ms\n"
                                            + "Max: " + str(max_ping) + "ms      "
                                            + "Min: " + str(min_ping) + "ms")
    legend = ax1.legend(loc='upper right')
    frame = legend.get_frame()
    frame.set_facecolor('1.00')
    upd_data()


def animate2():
    fig.canvas.mpl_connect('close_event', handle_close)
    fig.canvas.set_window_title('LoLPing v1.9a')
    ani = animation.FuncAnimation(fig, animate, frames=60)
    plt.show()

upd_data()
animate2()
