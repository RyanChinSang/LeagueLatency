import sys
import subprocess
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PIL import Image
from matplotlib import style
from datetime import datetime
from matplotlib.widgets import RadioButtons, Button

# A constant that forces Windows cmd to not generate a window when running the python subprocess through it
CREATE_NO_WINDOW = 0x08000000
# 'state' is used to keep track of weather the graph has been paused or not
state = 0
# Global arrays that keep the data for plotting the graphs
ltimes = []
lpings = []
avg_lis = []
# Global variables
avg = 0
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
servers = {"NA": "104.160.131.3", "LAN": "104.160.136.3"}
# matplotlib related variable initialization
style.use('seaborn-darkgrid')
fig = plt.figure(figsize=(16, 9))
ax1 = fig.add_subplot(1, 1, 1)
img = Image.open('pp_button.png')
img.thumbnail((64, 64), Image.ANTIALIAS)
icon_manager = matplotlib.pyplot.get_current_fig_manager()
icon_manager.window.wm_iconbitmap("icon.ico")
rax = plt.axes([0.881, 0.617, 0.089, 0.089], aspect='equal', frameon=True, axisbg='white')
radio = RadioButtons(rax, servers.keys())
radio_value = radio.value_selected


# class created to handle the buttons
class button_handler(object):
    ind = 0

    def quit(self, event):
        self.ind += 1
        handle_close(event)
        plt.draw()

    def pause(self, event):
        global state
        self.ind -= 1
        state += 1
        plt.draw()


# Function to correctly shutdown all processes of this program whenever closed by user
def handle_close(event):
    sys.exit()


# This function performs a Windows ping function and updates:
# 1- ping    : which is stored in global array pings each instance
# 2- time    : which is stored in global array ltimes each instance
# 3- avg     : hence also count and sum_ping (based on radio_value's "NA" or "LAN")
#            : which is stored in global array avg_lis each instance
# 4- max_ping: (based on radio_value's "NA" or "LAN")
# 5- min_ping: (based on radio_value's "NA" or "LAN")
def upd_data():
    global lpings, ltimes, sum_ping, servers, avg, avg_lis, radio_value
    global sum_ping_na, count_na, max_ping_na, min_ping_na
    global sum_ping_lan, count_lan, max_ping_lan, min_ping_lan
    # Recheck the radio button value so as to ping to the selected server
    radio_value = radio.value_selected
    p1 = subprocess.Popen(["ping.exe", servers[radio_value], "-n", "1", "-l", "500"],
                          stdout=subprocess.PIPE,
                          stdin=subprocess.PIPE,
                          stderr=subprocess.PIPE,
                          shell=False,
                          creationflags=CREATE_NO_WINDOW)
    # For instantaneous interpretation of output from subprocess
    while p1.poll() is None:
        line = p1.stdout.readline()
        # Data is updated in here from the newest subprocess ping
        if "time=" in line:
            ping = float(line[line.find("time=")+5:line.find("ms")])
            if radio_value == "NA":
                sum_ping_na += ping
                count_na += 1
                avg = sum_ping_na / count_na
                if ping > max_ping_na:
                    max_ping_na = ping
                if min_ping_na > ping:
                    min_ping_na = ping
            if radio_value == "LAN":
                sum_ping_lan += ping
                count_lan += 1
                avg = sum_ping_lan / count_lan
                if ping > max_ping_lan:
                    max_ping_lan = ping
                if min_ping_lan > ping:
                    min_ping_lan = ping
            avg_lis += [avg]
            lpings += [ping]
            interval = datetime.now() - start
            ltime = interval.total_seconds()
            ltimes += [ltime]


# This function does the 'graphical updating' based on the newly updated data from upd_date()
def animate(i):
    global max_ping, min_ping, ltimes, lpings, radio_value, servers, avg, avg_lis
    global sum_ping_na, count_na, max_ping_na, min_ping_na
    global sum_ping_lan, count_lan, max_ping_lan, min_ping_lan
    if radio_value == "NA":
        max_ping = max_ping_na
        min_ping = min_ping_na
    if radio_value == "LAN":
        max_ping = max_ping_lan
        min_ping = min_ping_lan
    ping_val = str(lpings[-1])
    time_val = str(ltimes[-1])
    yar = np.array(lpings)
    xar = np.array(ltimes)
    avgar = np.array(avg_lis)
    ax1.clear()
    ax1.text(0.999, 1.02, 'by Ryan Chin Sang', ha='right', va='top', color='0.85', size='small',
             transform=ax1.transAxes)
    # Positions of the first textbox to display data
    vpos_tb = 1.01
    hpos_tb = 0.973
    # Ping data
    if (0.9 * avg) <= float(ping_val) <= (1.1 * avg):
        ax1.text(vpos_tb, hpos_tb, "Ping: " + ping_val + " ms", transform=ax1.transAxes, linespacing=0.1,
                 bbox={'alpha': 0.23, 'pad': 5, "fc": "green", "ec": "green", "lw": 2})
    elif float(ping_val) > (1.1 * avg):
        ax1.text(vpos_tb, hpos_tb, "Ping: " + ping_val + " ms", transform=ax1.transAxes, linespacing=0.1,
                 bbox={'alpha': 0.3, 'pad': 5, "fc": "red", "lw": 2})
    else:
        ax1.text(vpos_tb, hpos_tb, "Ping: " + ping_val + " ms", transform=ax1.transAxes, linespacing=0.1,
                 bbox={'alpha': 0.14, 'pad': 5, "fc": "blue", "ec": "blue", "lw": 2})
    # Average dara
    if float(ping_val) < avg:
        ax1.text(vpos_tb, hpos_tb-0.05, "Avg: " + format(avg, '.3f') + " ms", transform=ax1.transAxes, linespacing=0.1,
                 bbox={'alpha': 0.23, 'pad': 5, "fc": "green", "ec": "green", "lw": 2})
    elif float(ping_val) > avg:
        ax1.text(vpos_tb, hpos_tb-0.05, "Avg: " + format(avg, '.3f') + " ms", transform=ax1.transAxes, linespacing=0.1,
                 bbox={'alpha': 0.3, 'pad': 5, "fc": "red", "lw": 2})
    else:
        ax1.text(vpos_tb, hpos_tb-0.05, "Avg: " + format(avg, '.3f') + " ms", transform=ax1.transAxes, linespacing=0.1,
                 bbox={'alpha': 0.14, 'pad': 5, "fc": "blue", "ec": "blue", "lw": 2})
    # Time data
    ax1.text(vpos_tb, hpos_tb-0.1, "Time: " + time_val + " s", transform=ax1.transAxes, linespacing=0.1,
             bbox={'alpha': 0.14, 'pad': 5, "fc": "blue", "ec": "blue", "lw": 2})
    # Maximum Ping data
    ax1.text(vpos_tb, hpos_tb-0.15, "Max: " + str(max_ping) + " ms", transform=ax1.transAxes, linespacing=0.1,
             bbox={'alpha': 0.14, 'pad': 5, "fc": "blue", "ec": "blue", "lw": 2})
    # Minimum Ping data
    ax1.text(vpos_tb, hpos_tb-0.2, "Min: " + str(min_ping) + " ms", transform=ax1.transAxes, linespacing=0.1,
             bbox={'alpha': 0.14, 'pad': 5, "fc": "blue", "ec": "blue", "lw": 2})
    # Shows state of the animated graph
    ax1.text(0.92, -0.0925, 'box', transform=ax1.transAxes, fontsize=22, zorder=0, color='white',
             bbox={'alpha': 0.2, 'pad': 5, "fc": "white", "ec": "black", "lw": 2})
    ax1.text(0.92, -0.087, '  Play' if state % 2 else 'Pause', transform=ax1.transAxes, zorder=1)
    ax1.set_ylabel('Ping /ms', size='large')
    ax1.set_xlabel('Time /s', size='large')
    ax1.set_title('Ping to League of Legends [' + radio_value + '] Server (' + servers[radio_value] + ')', fontsize=16,
                  fontweight='bold')
    ax1.plot(xar, yar, linewidth=1.0, label="Ping")
    ax1.plot(xar, avgar, linewidth=0.5, label="Average Ping")
    legend = ax1.legend(loc='upper left')
    # Only update the data if state indicates 'play' (opposite of button logic)
    if state % 2 == 0:
        upd_data()


# Sets the initial frame of the Window in which will be animated
def animate2():
    global state
    fig.canvas.mpl_connect('close_event', handle_close)
    fig.canvas.set_window_title('League Latency v2.1a')
    ani = animation.FuncAnimation(fig, animate, frames=120)
    # [(-=left, +=right), (-=up, +=down), (-=thin, +=wide), (-=thin, +=thick)]
    axquit = plt.axes([0.905, 0.01, 0.089, 0.05])
    bquit = Button(axquit, 'Quit')
    bquit.on_clicked(button_handler().quit)
    axpp = plt.axes([0.835, 0.01, 0.1, 0.05])
    bpp = Button(axpp, '', image=img)
    bpp.on_clicked(button_handler().pause)
    plt.show()

upd_data()
animate2()
