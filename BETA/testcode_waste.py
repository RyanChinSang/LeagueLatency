import os
import sys
import math
import errno
import subprocess
import tkMessageBox
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PIL import Image
from matplotlib import style
from datetime import datetime
from matplotlib.widgets import RadioButtons, Button

# Update the version of the program here:
version = "2.2a"
# 'state' is used to keep track of weather the graph has been paused or not
state = 0
# Global arrays that keep the data for plotting the graphs
ltimes = []
wtimes = []
btimes = []
lpings = []
wpings = []
bpings = []
avg_lis = []
top = []
bot = []
# Global variables
sd = 0
avg = 0
num_to = 0  # number of timeout errors
num_un = 0  # number of unreachable errors
sum_ping = 0
min_ping = float('+inf')
max_ping = float('-inf')
count_na = 0
sum_ping_na = 0
sum_sq_dif_na = 0
min_ping_na = float('+inf')
max_ping_na = float('-inf')
count_lan = 0
sum_ping_lan = 0
sum_sq_dif_lan = 0
min_ping_lan = float('+inf')
max_ping_lan = float('-inf')
start = datetime.now()
sq_dif_ar = []
servers = {"NA": "104.160.131.3", "LAN": "104.160.136.3"}
# matplotlib related variable initialization
style.use('seaborn-darkgrid')
fig = plt.figure(figsize=(16, 9))
ax1 = fig.add_subplot(1, 1, 1)
pp_img = Image.open(os.path.dirname(__file__) + '/static/buttons/pp_button.png')
dec_img = Image.open(os.path.dirname(__file__) + '/static/buttons/dec.png')
inc_img = Image.open(os.path.dirname(__file__) + '/static/buttons/inc.png')
null_img = Image.open(os.path.dirname(__file__) + '/static/buttons/null.png')
stgd_img = Image.open(os.path.dirname(__file__) + '/static/buttons/stgd.png')
stwr_img = Image.open(os.path.dirname(__file__) + '/static/buttons/stwr.png')
stbd_img = Image.open(os.path.dirname(__file__) + '/static/buttons/stbd.png')
unstgd_img = Image.open(os.path.dirname(__file__) + '/static/buttons/unstgd.png')
unstwr_img = Image.open(os.path.dirname(__file__) + '/static/buttons/unstwr.png')
unstbd_img = Image.open(os.path.dirname(__file__) + '/static/buttons/unstbd.png')
unstlgd_img = Image.open(os.path.dirname(__file__) + '/static/buttons/unstlgd.png')
unstlwr_img = Image.open(os.path.dirname(__file__) + '/static/buttons/unstlwr.png')
unstlbd_img = Image.open(os.path.dirname(__file__) + '/static/buttons/unstlbd.png')
vunstgd_img = Image.open(os.path.dirname(__file__) + '/static/buttons/vunstgd.png')
vunstwr_img = Image.open(os.path.dirname(__file__) + '/static/buttons/vunstwr.png')
vunstbd_img = Image.open(os.path.dirname(__file__) + '/static/buttons/vunstbd.png')
pp_img.thumbnail((64, 64), Image.ANTIALIAS)
dec_img.thumbnail((16, 16), Image.ANTIALIAS)
inc_img.thumbnail((16, 16), Image.ANTIALIAS)
stgd_img.thumbnail((16, 16), Image.ANTIALIAS)
stwr_img.thumbnail((16, 16), Image.ANTIALIAS)
stbd_img.thumbnail((16, 16), Image.ANTIALIAS)
unstgd_img.thumbnail((16, 16), Image.ANTIALIAS)
unstwr_img.thumbnail((16, 16), Image.ANTIALIAS)
unstbd_img.thumbnail((16, 16), Image.ANTIALIAS)
unstlgd_img.thumbnail((16, 16), Image.ANTIALIAS)
unstlwr_img.thumbnail((16, 16), Image.ANTIALIAS)
unstlbd_img.thumbnail((16, 16), Image.ANTIALIAS)
vunstgd_img.thumbnail((16, 16), Image.ANTIALIAS)
vunstwr_img.thumbnail((16, 16), Image.ANTIALIAS)
vunstbd_img.thumbnail((16, 16), Image.ANTIALIAS)
icon_manager = mpl.pyplot.get_current_fig_manager()
icon_manager.window.wm_iconbitmap(os.path.dirname(__file__) + '/static/icons/icon.ico')
rax = plt.axes([0.881, 0.535, 0.089, 0.089], aspect='equal', frameon=True, axisbg='white')
radio = RadioButtons(rax, servers.keys())
radio_value = radio.value_selected


class ButtonHandler(object):
    """
    Class created to handle button functionality via .on_clicked()
    """
    ind = 0

    def quit(self, event):
        self.ind += 1
        close_handler(event)
        plt.draw()

    def pause(self, event):
        global state
        self.ind -= 1
        state += 1
        plt.draw()


def make_databox(vpos, hpos, alpha, fc, ec):
    """
    Creates a box of all equal dimensions to hold the text data at the side of the graph - uniformity!
    vpos: vertical position float
    hpos: horizontal position float
    alpha: strength of the colour float
    colour: colour of the box string
    """
    return ax1.text(vpos, hpos, '______________.', transform=ax1.transAxes, alpha=0,
                    bbox={'alpha': alpha,
                          'pad': 5,
                          "fc": fc,
                          "ec": ec,
                          "lw": 2})


def close_handler(event):
    """
    Safely shutdown all processes of this program whenever the window is closed by user.
    """
    sys.exit()


def spperr_handler(err):
    """
    Sub-process ping error handler
    Handles common 'errors' we can expect from Window's ping.exe, which is accessed through a subprocess.
    'errors' refer to unsuccessful pings.
    """
    err_dict = {'Destination host unreachable': 'The destination was unreachable!\nPlease check your internet '
                                                'connection and press Retry.',
                'Request timed out': 'The destination took too long to respond!\nPlease check your internet connection '
                                     'and press Retry.'
                }
    try:
        if tkMessageBox.askretrycancel(err, err_dict[err]):
            upd_data()
        else:
            sys.exit()
    # This should never occur - this handles errors not in the err_dict (the expected errors).
    # Could be useful if a very powerful err_handler was coded, where every line is passed through here.
    except KeyError:
        if tkMessageBox.showerror('Unknown Error', 'The condition under which this error occurred was unexpected!'):
            sys.exit()


def set_savdir(sav_dir='Screenshots'):
    """
    Configures the default mpl save directory for screenshots.
    Checks if there is a folder named 'Screenshots' in root folder.
    If there is no folder there named 'Screenshots', it creates the directory.
    """
    if not os.path.isdir(os.path.join(os.path.dirname(__file__), sav_dir).replace('\\', '/')):
        try:
            os.makedirs(os.path.join(os.path.dirname(__file__), sav_dir).replace('\\', '/'))
        except OSError as exc:
            if not (exc.errno == errno.EEXIST and os.path.isdir(os.path.join(os.path.dirname(__file__),
                                                                             sav_dir).replace('\\', '/'))):
                raise
    # Now that the directory for 'Screenshots' surely exists, set it as default directory.
    mpl.rcParams["savefig.directory"] = os.path.join(os.path.dirname(__file__), sav_dir).replace('\\', '/')


def draw_ping(vpos, hpos, ping, up_bound, lo_bound, stdv, vpos_tb, hpos_tb, a_yellow, a_green, a_red):
    """
    A powerful function that performs:
    1- The specification of the databox which holds the ping data:
       a. Inner (face) colour represents the ping range
       b. Outer (edge) colour represents the ping state (spiked, below lo_bound etc.)
    2- Drawing the circle that summarizes the state of the ping
    vpos: the vertical position of the button it draws the ping circle in
    hpos: the horizontal position of the button it draws the ping circle in
    ping: the value of the current ping
          used in data analysis and is a key factor to decide the state of the ping
    up_bound: represents the ping + standard deviation
    lo_bound: represents the ping - standard deviation
    stdv: the standard deviation calculated in upd_data(), passed from animate(i)
    vpos_tb: the vertical position of the databox which holds the ping data
    hpos_tb: the horizontal position of the databox which holds the ping data
    a_yellow: the strength of the databox colour for yellow
    a_green: the strength of the databox colour for green
    a_red:  the strength of the databox colour for red
    """
    global avg
    # Ping is 'good'
    if 0 <= ping <= 199:
        # Ping is very unstable - has very large and frequent spikes
        if stdv * 2 >= 0.3 * avg:
            make_databox(vpos=vpos_tb, hpos=hpos_tb, alpha=a_green, fc="green", ec="red")
            return Button(plt.axes([hpos, vpos, 0.02, 0.02]), '', image=vunstgd_img, color='None')
        # Ping is unstable - has a few frequent medium spikes causing the range to go over 15% current average ping
        elif stdv * 2 >= 0.15 * avg:
            make_databox(vpos=vpos_tb, hpos=hpos_tb, alpha=a_green, fc="green", ec="gold")
            return Button(plt.axes([hpos, vpos, 0.02, 0.02]), '', image=unstgd_img, color='None')
        # Ping is stable
        elif lo_bound <= ping <= up_bound:
            make_databox(vpos=vpos_tb, hpos=hpos_tb, alpha=a_green, fc="green", ec="green")
            return Button(plt.axes([hpos, vpos, 0.02, 0.02]), '', image=stgd_img, color='None')
        # Ping is out of bounds (unstable)
        else:
            # If ping is lower than lower bound, then all conditions tend toward a better ping - colour this as blue
            if ping <= lo_bound:
                make_databox(vpos=vpos_tb, hpos=hpos_tb, alpha=a_green, fc="green", ec="blue")
                return Button(plt.axes([hpos, vpos, 0.02, 0.02]), '', image=unstlgd_img, color='None')
            # Else it is simply just unstable
            else:
                make_databox(vpos=vpos_tb, hpos=hpos_tb, alpha=a_green, fc="green", ec="gold")
                return Button(plt.axes([hpos, vpos, 0.02, 0.02]), '', image=unstgd_img, color='None')
    # Ping is 'not good'
    elif 200 <= ping <= 499:
        if stdv * 2 >= 0.3 * avg:
            make_databox(vpos=vpos_tb, hpos=hpos_tb, alpha=a_yellow, fc="yellow", ec="red")
            return Button(plt.axes([hpos, vpos, 0.02, 0.02]), '', image=vunstwr_img, color='None')
        elif stdv * 2 >= 0.15 * avg:
            make_databox(vpos=vpos_tb, hpos=hpos_tb, alpha=a_yellow, fc="yellow", ec="gold")
            return Button(plt.axes([hpos, vpos, 0.02, 0.02]), '', image=unstgd_img, color='None')
        elif lo_bound <= ping <= up_bound:
            make_databox(vpos=vpos_tb, hpos=hpos_tb, alpha=a_yellow, fc="yellow", ec="green")
            return Button(plt.axes([hpos, vpos, 0.02, 0.02]), '', image=stwr_img, color='None')
        else:
            if ping <= lo_bound:
                make_databox(vpos=vpos_tb, hpos=hpos_tb, alpha=a_yellow, fc="yellow", ec="blue")
                return Button(plt.axes([hpos, vpos, 0.02, 0.02]), '', image=unstlwr_img, color='None')
            else:
                make_databox(vpos=vpos_tb, hpos=hpos_tb, alpha=a_yellow, fc="yellow", ec="gold")
                return Button(plt.axes([hpos, vpos, 0.02, 0.02]), '', image=unstwr_img, color='None')
    # Ping is 'bad'
    elif ping > 500:
        if stdv * 2 >= 0.3 * avg:
            make_databox(vpos=vpos_tb, hpos=hpos_tb, alpha=a_red, fc="red", ec="black")
            return Button(plt.axes([hpos, vpos, 0.02, 0.02]), '', image=vunstbd_img, color='None')
        elif stdv * 2 >= 0.15 * avg:
            make_databox(vpos=vpos_tb, hpos=hpos_tb, alpha=a_red, fc="red", ec="gold")
            return Button(plt.axes([hpos, vpos, 0.02, 0.02]), '', image=unstgd_img, color='None')
        elif lo_bound <= ping <= up_bound:
            make_databox(vpos=vpos_tb, hpos=hpos_tb, alpha=a_red, fc="red", ec="green")
            return Button(plt.axes([hpos, vpos, 0.02, 0.02]), '', image=stbd_img, color='None')
        else:
            if ping <= lo_bound:
                make_databox(vpos=vpos_tb, hpos=hpos_tb, alpha=a_red, fc="red", ec="blue")
                return Button(plt.axes([hpos, vpos, 0.02, 0.02]), '', image=unstlbd_img, color='None')
            else:
                make_databox(vpos=vpos_tb, hpos=hpos_tb, alpha=a_red, fc="red", ec="gold")
                return Button(plt.axes([hpos, vpos, 0.02, 0.02]), '', image=unstbd_img, color='None')


def upd_data():
    """
    This function performs a Windows ping function and updates:
    1- lping   : which is stored in global data array lpings each instance
               : if lping >= 200 or <= 499, it is stored in global data array wpings each instance
               : if lping >= 500, it is stored in global data array bpings each instance
    2- ltime   : which is stored in global data array ltimes each instance
               : is stored in global data array wtimes each instance wpings has a new value
               : is stored in global data array btimes each instance wpings has a new value
    3- avg     : hence also count and sum_ping (based on radio_value's "NA" or "LAN")
               : which is stored in global array avg_lis each instance
    4- max_ping: (based on radio_value's "NA" or "LAN")
    5- min_ping: (based on radio_value's "NA" or "LAN")
    6- sd      : the standard deviation (lping-avg)^2/count (based on radio_value's "NA" or "LAN")
               : used to calculate top (upper bound = avg + sd) and bot (lower bound = avg - sd)
               : top and bot are global data arrays
    Notes:
        1- creationflags=0x08000000 (for subprocess) forces Windows cmd to not generate a window.
    """
    global lpings, ltimes, sum_ping, servers, avg, avg_lis, radio_value, num_un, num_to, top, bot, sd, wtimes, wpings, \
        bpings, btimes
    global sum_ping_na, count_na, max_ping_na, min_ping_na, sum_sq_dif_na
    global sum_ping_lan, count_lan, max_ping_lan, min_ping_lan, sum_sq_dif_lan
    # Recheck the radio button value so as to ping to the selected server
    radio_value = radio.value_selected
    sp = subprocess.Popen(["ping.exe", servers[radio_value], "-n", "1", "-l", "500"],
                          stdout=subprocess.PIPE,
                          stdin=subprocess.PIPE,
                          stderr=subprocess.PIPE,
                          shell=False,
                          creationflags=0x08000000)
    # For instantaneous interpretation of output from subprocess
    while sp.poll() is None:
        line = sp.stdout.readline()
        # Data is updated in here from the newest subprocess ping
        if "time=" in line:
            lping = float(line[line.find("time=")+5:line.find("ms")])
            if radio_value == "NA":
                sum_ping_na += lping
                count_na += 1
                avg = sum_ping_na / count_na
                sq_dif = (lping - avg)*(lping - avg)
                sum_sq_dif_na += sq_dif
                sd = math.sqrt(sum_sq_dif_na / count_na)
                if lping > max_ping_na:
                    max_ping_na = lping
                if min_ping_na > lping:
                    min_ping_na = lping
            if radio_value == "LAN":
                sum_ping_lan += lping
                count_lan += 1
                avg = sum_ping_lan / count_lan
                sq_dif = (lping - avg) * (lping - avg)
                sum_sq_dif_lan += sq_dif
                sd = math.sqrt(sum_sq_dif_lan / count_lan)
                if lping > max_ping_lan:
                    max_ping_lan = lping
                if min_ping_lan > lping:
                    min_ping_lan = lping
            top += [avg + sd]
            bot += [avg - sd]
            avg_lis += [avg]
            interval = datetime.now() - start
            ltime = interval.total_seconds()
            ltimes += [ltime]
            lpings += [lping]
            if 200 <= lping <= 499:
                wpings += [lping]
                wtimes += [ltime]
            elif lping >= 500:
                bpings += [lping]
                btimes += [ltime]
        elif "Destination host unreachable" in line:
            num_un += 1
            spperr_handler("Destination host unreachable")
        elif "Request timed out" in line:
            num_to += 1
            spperr_handler("Request timed out")


def animate(i):
    """
    Performs the 'graphical updating' based on the newly updated data from upd_date()
    """
    global max_ping, min_ping, ltimes, lpings, radio_value, servers, avg, avg_lis, num_to, num_un, top, bot, wtimes,\
        wpings, btimes
    global sum_ping_na, count_na, max_ping_na, min_ping_na
    global sum_ping_lan, count_lan, max_ping_lan, min_ping_lan
    if radio_value == "NA":
        max_ping = max_ping_na
        min_ping = min_ping_na
    if radio_value == "LAN":
        max_ping = max_ping_lan
        min_ping = min_ping_lan
    pingar = np.array(lpings)
    timear = np.array(ltimes)
    w_pingar = np.array(wpings)
    w_timear = np.array(wtimes)
    b_pingar = np.array(bpings)
    b_timear = np.array(btimes)
    avgar = np.array(avg_lis)
    topar = np.array(top)
    botar = np.array(bot)
    ax1.clear()
    ax1.text(0.999, 1.02, 'by Ryan Chin Sang', ha='right', va='top', color='0.85', size='small',
             transform=ax1.transAxes)
    # Positions of the first textbox to display data
    vpos_tb = 1.01
    hpos_tb = 0.973
    hpos_img = 0.88
    vpos_img = 0.8325
    a_red = 0.3
    a_grey = 0.2
    a_blue = 0.14
    a_green = 0.23
    a_yellow = 0.17
    # Ping data
    ax1.text(vpos_tb, hpos_tb, "Ping: " + str(lpings[-1]) + " ms", transform=ax1.transAxes)
    draw_ping(vpos=vpos_img + 0.0385, hpos=hpos_img, ping=lpings[-1], up_bound=top[-1], lo_bound=bot[-1], stdv=sd,
              vpos_tb=vpos_tb, hpos_tb=hpos_tb, a_green=a_green, a_red=a_red, a_yellow=a_yellow)
    # Average ping
    if lpings[-1] < avg:
        make_databox(vpos=vpos_tb, hpos=hpos_tb - 0.05, alpha=a_green, fc="green", ec="green")
        ax1.text(vpos_tb, hpos_tb-0.05, "Avg: " + format(avg, '.3f') + " ms", transform=ax1.transAxes)
        Button(plt.axes([hpos_img, vpos_img, 0.02, 0.02]), '', image=dec_img, color='None')
    elif lpings[-1] > avg:
        make_databox(vpos=vpos_tb, hpos=hpos_tb - 0.05, alpha=a_red, fc="red", ec="black")
        ax1.text(vpos_tb, hpos_tb - 0.05, "Avg: " + format(avg, '.3f') + " ms", transform=ax1.transAxes)
        Button(plt.axes([hpos_img, vpos_img, 0.02, 0.02]), '', image=inc_img, color='None')
    else:
        make_databox(vpos=vpos_tb, hpos=hpos_tb - 0.05, alpha=a_blue, fc="blue", ec="blue")
        ax1.text(vpos_tb, hpos_tb - 0.05, "Avg: " + format(avg, '.3f') + " ms", transform=ax1.transAxes)
        Button(plt.axes([hpos_img, vpos_img, 0.02, 0.02]), '', image=null_img, color='None')
    # Time data
    make_databox(vpos=vpos_tb, hpos=hpos_tb - 0.1, alpha=a_blue, fc="blue", ec="blue")
    ax1.text(vpos_tb, hpos_tb-0.1, "Time: " + str(ltimes[-1]) + " s", transform=ax1.transAxes)
    # Maximum Ping data
    make_databox(vpos=vpos_tb, hpos=hpos_tb - 0.15, alpha=a_blue, fc="blue", ec="blue")
    ax1.text(vpos_tb, hpos_tb-0.15, "Max: " + str(max_ping) + " ms", transform=ax1.transAxes)
    # Minimum Ping data
    make_databox(vpos=vpos_tb, hpos=hpos_tb - 0.2, alpha=a_blue, fc="blue", ec="blue")
    ax1.text(vpos_tb, hpos_tb-0.2, "Min: " + str(min_ping) + " ms", transform=ax1.transAxes)
    # No. of timeouts
    make_databox(vpos=vpos_tb, hpos=hpos_tb - 0.25, alpha=a_grey, fc="grey", ec="black")
    ax1.text(vpos_tb, hpos_tb-0.25, "# Timeout: " + str(num_to), transform=ax1.transAxes)
    # No. of unreachables
    make_databox(vpos=vpos_tb, hpos=hpos_tb - 0.3, alpha=a_grey, fc="grey", ec="black")
    ax1.text(vpos_tb, hpos_tb-0.3, "# Unreachable: " + str(num_un), transform=ax1.transAxes)
    # Shows state of the animated graph
    ax1.text(0.92, -0.0925, 'box', transform=ax1.transAxes, fontsize=22, zorder=0, alpha=0,
             bbox={'alpha': a_grey, 'pad': 5, "fc": "white", "ec": "black", "lw": 2})
    ax1.text(0.92, -0.087, '  Play' if state % 2 else 'Pause', transform=ax1.transAxes, zorder=1)
    ax1.set_ylabel('Ping /ms', size='large')
    ax1.set_xlabel('Time /s', size='large')
    ax1.set_title('Ping to League of Legends [' + radio_value + '] Server (' + servers[radio_value] + ')', fontsize=16,
                  fontweight='bold')
    ax1.plot(timear, pingar, linewidth=1.0, label="Ping")
    ax1.plot(timear, avgar, linewidth=0.6, label="Average Ping")
    # Draws a yellow graph when ping goes over 200 ms and is less than 499 ms
    ax1.plot(w_timear, w_pingar, linewidth=1.5, color='yellow', zorder=1)
    # Draws a red graph when ping goes over 500 ms
    ax1.plot(b_timear, b_pingar, linewidth=1.5, color='red', zorder=1)
    ax1.plot(timear, topar, linewidth=0.3)
    ax1.plot(timear, botar, linewidth=0.3)
    ax1.fill_between(timear, botar, topar, facecolor='green', interpolate=True, alpha=0.0375)
    ax1.legend(loc='upper left')
    # Only update the data if state indicates 'play' (opposite of button logic)
    if state % 2 == 0:
        upd_data()


def set_frame():
    """
    Sets the initial frame of the Window in which will be animated through animate(i)
    """
    global state
    fig.canvas.mpl_connect('close_event', close_handler)
    fig.canvas.set_window_title('League Latency v' + version)
    ani = animation.FuncAnimation(fig, animate, frames=120)
    # [(-=left, +=right), (-=up, +=down), (-=thin, +=wide), (-=thin, +=thick)]
    quit_b = Button(plt.axes([0.905, 0.01, 0.089, 0.05]), 'Quit')
    quit_b.on_clicked(ButtonHandler().quit)
    pp_b = Button(plt.axes([0.835, 0.01, 0.1, 0.05]), '', image=pp_img)
    pp_b.on_clicked(ButtonHandler().pause)
    plt.show()

set_savdir()
upd_data()
set_frame()
