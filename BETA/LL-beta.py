# Perform all experimental code here. When stable copy over to the stable folder as 'LL.py'.

import os
import sys
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
version = "2.4a BETA"
# 'state' is used to keep track of weather the graph has been paused or not
state = 0
# Global arrays that keep the data for plotting the graphs
nppings_lan = np.array([])
nppings_na = np.array([])
nppings = np.array([])
nptimes = np.array([])
npavgs = np.array([])
nptop = np.array([])
npbot = np.array([])
font = 'Agency FB'
# Global variables
sd = 0
avg = 0
num_to = 0  # number of timeout errors
num_un = 0  # number of unreachable errors
min_ping = float('+inf')
max_ping = float('-inf')
min_ping_na = float('+inf')
max_ping_na = float('-inf')
min_ping_lan = float('+inf')
max_ping_lan = float('-inf')
start = datetime.now()
servers = {"NA": "104.160.131.3", "LAN": "104.160.136.3"}
# matplotlib-related variable initializations
style.use('seaborn-darkgrid')
fig = plt.figure(figsize=(16, 9))
ax1 = fig.add_subplot(1, 1, 1)
mpl.rcParams["font.family"] = font
mpl.rcParams["font.size"] = 13
pp_img = Image.open(os.path.dirname(__file__) + '/static/buttons/pp_button.png')
pl_img = Image.open(os.path.dirname(__file__) + '/static/buttons/pl_button.png')
pa_img = Image.open(os.path.dirname(__file__) + '/static/buttons/pa_button.png')
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
pp_img.thumbnail((128, 128), Image.ANTIALIAS)
pl_img.thumbnail((55, 55), Image.ANTIALIAS)
pa_img.thumbnail((55, 55), Image.ANTIALIAS)
dec_img.thumbnail((32, 32), Image.ANTIALIAS)
inc_img.thumbnail((32, 32), Image.ANTIALIAS)
stgd_img.thumbnail((32, 32), Image.ANTIALIAS)
stwr_img.thumbnail((32, 32), Image.ANTIALIAS)
stbd_img.thumbnail((32, 32), Image.ANTIALIAS)
unstgd_img.thumbnail((32, 32), Image.ANTIALIAS)
unstwr_img.thumbnail((32, 32), Image.ANTIALIAS)
unstbd_img.thumbnail((32, 32), Image.ANTIALIAS)
unstlgd_img.thumbnail((32, 32), Image.ANTIALIAS)
unstlwr_img.thumbnail((32, 32), Image.ANTIALIAS)
unstlbd_img.thumbnail((32, 32), Image.ANTIALIAS)
vunstgd_img.thumbnail((32, 32), Image.ANTIALIAS)
vunstwr_img.thumbnail((32, 32), Image.ANTIALIAS)
vunstbd_img.thumbnail((32, 32), Image.ANTIALIAS)
icon_manager = mpl.pyplot.get_current_fig_manager()
icon_manager.window.wm_iconbitmap(os.path.dirname(__file__) + '/static/icons/icon.ico')
rax1 = plt.axes([0.881, 0.535, 0.089, 0.089], aspect='equal', frameon=False, facecolor='gray')
radio = RadioButtons(rax1, servers.keys())
radio_value = radio.value_selected


# Object definitons
class ButtonHandler(object):
    """
    Class created to handle button functionality via the .on_clicked() method.
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


# Function defintions
def close_handler(event):
    """
    Safely shutdown all processes of this program whenever the window is closed by user.
    """
    sys.exit()


def make_textbox(vpos, hpos, alpha, fc, ec):
    """
    Creates a box of all equal dimensions to hold the text data at the side of the graph - uniformity!

    vpos  : vertical position float
    hpos  : horizontal position float
    alpha : strength of the colour float
    colour: colour of the box string
    """
    return ax1.text(vpos, hpos, '______________.', transform=ax1.transAxes, alpha=0,
                    bbox={'alpha': alpha,
                          'pad': 5,
                          "fc": fc,
                          "ec": ec,
                          "lw": 2})


def spperr_handler(err):
    """
    Sub-Process Ping ERRor (SPPERR) handler
    Handles common 'errors' we can expect from Window's ping.exe, which is accessed through a subprocess.

    err: a string that is likely listed as a key in the defined err_dict dictionary

    Notes:
        1- 'errors' refer to any and all unsuccessful pings.
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
    This function performs:
    1- Configures the default mpl save directory for screenshots.
    2- Checks if there is a folder named 'Screenshots' in root folder.
       a. If there is no folder in the root folder named 'Screenshots', it creates the directory.
       b. If the folder is there, then set it as the default directory.

    sav_dir: the name of the folder in which all screenshots will be saved to (and set as default)
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
    1- The specification of the textbox (cred via make_textbox() function) which holds the ping data:
       a. Inner (face) colour represents the ping range
       b. Outer (edge) colour represents the ping state (spiked, below lo_bound etc.)
    2- Drawing the circle that summarizes the state of the ping

    vpos    : the vertical position of the button it draws the ping circle in
    hpos    : the horizontal position of the button it draws the ping circle in
    ping    : the value of the current ping
          NB: Used in data analysis and is a key factor to decide the state of the ping
    up_bound: represents the ping + standard deviation
    lo_bound: represents the ping - standard deviation
    stdv    : the standard deviation calculated in upd_data(), passed from animate(i)
    vpos_tb : the vertical position of the textbox which holds the ping data
    hpos_tb : the horizontal position of the textbox which holds the ping data
    a_yellow: the strength of the textbox colour for yellow
    a_green : the strength of the textbox colour for green
    a_red   : the strength of the textbox colour for red
    """
    global avg
    # Ping is 'good'
    if ping < 200:
        # Ping is very unstable - has very large and frequent spikes
        if stdv * 2 >= 0.3 * avg:
            make_textbox(vpos=vpos_tb, hpos=hpos_tb, alpha=a_green, fc="green", ec="red")
            return Button(plt.axes([hpos, vpos, 0.02, 0.02]), '', image=vunstgd_img, color='None')
        # Ping is unstable - has a few frequent medium spikes causing the range to go over 15% current average ping
        elif stdv * 2 >= 0.15 * avg:
            make_textbox(vpos=vpos_tb, hpos=hpos_tb, alpha=a_green, fc="green", ec="gold")
            return Button(plt.axes([hpos, vpos, 0.02, 0.02]), '', image=unstgd_img, color='None')
        # Ping is stable
        elif lo_bound <= ping <= up_bound:
            make_textbox(vpos=vpos_tb, hpos=hpos_tb, alpha=a_green, fc="green", ec="green")
            return Button(plt.axes([hpos, vpos, 0.02, 0.02]), '', image=stgd_img, color='None')
        # Ping is out of bounds (unstable)
        else:
            # If ping is lower than lower bound, then all conditions tend toward a better ping - colour this as blue
            if ping <= lo_bound:
                make_textbox(vpos=vpos_tb, hpos=hpos_tb, alpha=a_green, fc="green", ec="blue")
                return Button(plt.axes([hpos, vpos, 0.02, 0.02]), '', image=unstlgd_img, color='None')
            # Else it is simply just unstable
            else:
                make_textbox(vpos=vpos_tb, hpos=hpos_tb, alpha=a_green, fc="green", ec="gold")
                return Button(plt.axes([hpos, vpos, 0.02, 0.02]), '', image=unstgd_img, color='None')
    # Ping is 'not good'
    elif 200 <= ping <= 500:
        if stdv * 2 >= 0.3 * avg:
            make_textbox(vpos=vpos_tb, hpos=hpos_tb, alpha=a_yellow, fc="yellow", ec="red")
            return Button(plt.axes([hpos, vpos, 0.02, 0.02]), '', image=vunstwr_img, color='None')
        elif stdv * 2 >= 0.15 * avg:
            make_textbox(vpos=vpos_tb, hpos=hpos_tb, alpha=a_yellow, fc="yellow", ec="gold")
            return Button(plt.axes([hpos, vpos, 0.02, 0.02]), '', image=unstgd_img, color='None')
        elif lo_bound <= ping <= up_bound:
            make_textbox(vpos=vpos_tb, hpos=hpos_tb, alpha=a_yellow, fc="yellow", ec="green")
            return Button(plt.axes([hpos, vpos, 0.02, 0.02]), '', image=stwr_img, color='None')
        else:
            if ping <= lo_bound:
                make_textbox(vpos=vpos_tb, hpos=hpos_tb, alpha=a_yellow, fc="yellow", ec="blue")
                return Button(plt.axes([hpos, vpos, 0.02, 0.02]), '', image=unstlwr_img, color='None')
            else:
                make_textbox(vpos=vpos_tb, hpos=hpos_tb, alpha=a_yellow, fc="yellow", ec="gold")
                return Button(plt.axes([hpos, vpos, 0.02, 0.02]), '', image=unstwr_img, color='None')
    # Ping is 'bad'
    elif ping > 500:
        if stdv * 2 >= 0.3 * avg:
            make_textbox(vpos=vpos_tb, hpos=hpos_tb, alpha=a_red, fc="red", ec="black")
            return Button(plt.axes([hpos, vpos, 0.02, 0.02]), '', image=vunstbd_img, color='None')
        elif stdv * 2 >= 0.15 * avg:
            make_textbox(vpos=vpos_tb, hpos=hpos_tb, alpha=a_red, fc="red", ec="gold")
            return Button(plt.axes([hpos, vpos, 0.02, 0.02]), '', image=unstgd_img, color='None')
        elif lo_bound <= ping <= up_bound:
            make_textbox(vpos=vpos_tb, hpos=hpos_tb, alpha=a_red, fc="red", ec="green")
            return Button(plt.axes([hpos, vpos, 0.02, 0.02]), '', image=stbd_img, color='None')
        else:
            if ping <= lo_bound:
                make_textbox(vpos=vpos_tb, hpos=hpos_tb, alpha=a_red, fc="red", ec="blue")
                return Button(plt.axes([hpos, vpos, 0.02, 0.02]), '', image=unstlbd_img, color='None')
            else:
                make_textbox(vpos=vpos_tb, hpos=hpos_tb, alpha=a_red, fc="red", ec="gold")
                return Button(plt.axes([hpos, vpos, 0.02, 0.02]), '', image=unstbd_img, color='None')


def link(data1, data2):
    """
    The function performs:
    1- Linking data1 to data2 for where there are matches in both index and value between data1 and data2
       ie. surround data1's values with the values in data2
       a. This allows the graph to be segmented by linking the segments to eachother.

    data1: non-empty array whose values are to be linked to data2
    data2: non-empty array whose values are used to link data1's values
       NB: This is usually a much 'fuller' array than data2

    Notes:
        1- data1 and data2 must be lists of same datatype and of equal size.
        2- 'fuller' refers to less non-values in the array (i.e. more real values) compared to the other array
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


def draw_zones(yax_min, yax_max):
    """
    Colours the horizontal zones in the colour that represents the quality of the ping.
    """
    # Red i.e. 'bad' ping zone
    if yax_max > 500:
        ax1.axhspan(yax_min, 200, fc='green', ec='none', alpha=0.10)
        ax1.axhspan(200, 500, fc='yellow', ec='none', alpha=0.10)
        ax1.axhspan(500, yax_max, fc='red', ec='none', alpha=0.10)
    # Yellow i.e. 'not good' ping zone
    elif yax_max > 200:
        ax1.axhspan(yax_min, 200, fc='green', ec='none', alpha=0.10)
        ax1.axhspan(200, yax_max, fc='yellow', ec='none', alpha=0.10)
    # Green i.e. 'good' ping zone
    else:
        ax1.axhspan(yax_min, yax_max, fc='green', ec='none', alpha=0.10)


def upd_data():
    """
    This function performs a standard command prompt Windows ping function and updates:
    1- nppings : which is stored in global numpy array nppings each instance
            NB1: nppings stores all ping values and is used for plotting
            NB2: nppings_xx stores all ping values for radio_value's "xx" and is used for statistical calculations
    2- nptimes : which is stored in global numpy array nptimes each instance
               : is used for plotting all graphs with respect to time
    3- avg     : (based on radio_value's "NA" or "LAN")
               : which is stored in global numpy array npavgs each instance
    4- max_ping: (based on radio_value's "NA" or "LAN")
    5- min_ping: (based on radio_value's "NA" or "LAN")
    6- sd      : the standard deviation (based on radio_value's "NA" or "LAN")
               : used to calculate nptop (upper bound = avg + sd) and npbot (lower bound = avg - sd) values
               : nptop and npbot are global numpy arrays

    Notes:
        1- creationflags=0x08000000 (for subprocess) forces Windows cmd to not generate a window.
    """
    global servers, avg, radio_value, num_un, num_to, sd
    global nppings, nppings_na, nppings_lan, nptimes, npavgs, nptop, npbot
    global max_ping_na, min_ping_na
    global max_ping_lan, min_ping_lan
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
            nppings = np.append(nppings, [float(line[line.find("time=")+5:line.find("ms")])])
            interval = datetime.now() - start
            nptimes = np.append(nptimes, [interval.total_seconds()])
            if radio_value == "NA":
                nppings_na = np.append(nppings_na, [float(line[line.find("time=") + 5:line.find("ms")])])
                max_ping_na = nppings_na.max()
                min_ping_na = nppings_na.min()
                avg = np.average(nppings_na)
                sd = np.std(nppings_na, dtype=np.float32, axis=0)
            if radio_value == "LAN":
                nppings_lan = np.append(nppings_lan, [float(line[line.find("time=") + 5:line.find("ms")])])
                max_ping_lan = nppings_lan.max()
                min_ping_lan = nppings_lan.min()
                avg = np.average(nppings_lan)
                sd = np.std(nppings_lan, dtype=np.float32, axis=0)
            nptop = np.append(nptop, [avg + sd])
            npbot = np.append(npbot, [avg - sd])
            npavgs = np.append(npavgs, [avg])
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
    global max_ping, min_ping, radio_value, servers, avg, num_to, num_un
    global nppings, nptimes, npavgs, nptop, npbot
    global max_ping_na, min_ping_na
    global max_ping_lan, min_ping_lan
    if radio_value == "NA":
        max_ping = max_ping_na
        min_ping = min_ping_na
    if radio_value == "LAN":
        max_ping = max_ping_lan
        min_ping = min_ping_lan
    # Make 3 copies of the pings for making green, yellow and red plots
    gpings = nppings.copy()
    ypings = nppings.copy()
    rpings = nppings.copy()
    # For green plot points, keep all values < 200, set the rest to a non-point
    gpings[gpings > 200] = np.nan
    # For yellow plot points, keep all values > 200 and < 500, then link adjacent points
    ypings[ypings <= 200] = 0
    ypings[ypings >= 500] = 0
    ypings[ypings == 0] = np.nan
    link(ypings, nppings)
    # For red plot points, keep all values > 500, then link adjacent points
    rpings[rpings < 500] = np.nan
    link(rpings, nppings)

    ax1.clear()
    ax1.text(0.999, 1.02, 'by Ryan Chin Sang', ha='right', va='top', color='0.85', size='x-small',
             transform=ax1.transAxes)
    # Positions of the first textbox to display data
    vpos_tb = 1.01
    hpos_tb = 0.973
    hpos_img = 0.88  # -ve = left
    vpos_img = 0.815  # -ve = down
    a_red = 0.3
    a_grey = 0.2
    a_blue = 0.14
    a_green = 0.23
    a_yellow = 0.17
    # Ping data
    ax1.text(vpos_tb, hpos_tb, "Ping: " + str(nppings[-1]) + " ms", transform=ax1.transAxes)
    draw_ping(vpos=vpos_img + 0.0385, hpos=hpos_img, ping=nppings[-1], up_bound=nptop[-1], lo_bound=npbot[-1], stdv=sd,
              vpos_tb=vpos_tb, hpos_tb=hpos_tb, a_green=a_green, a_red=a_red, a_yellow=a_yellow)
    # Average ping
    if nppings[-1] < avg:
        make_textbox(vpos=vpos_tb, hpos=hpos_tb - 0.05, alpha=a_green, fc="green", ec="green")
        ax1.text(vpos_tb, hpos_tb-0.05, "Avg: " + format(avg, '.3f') + " ms", transform=ax1.transAxes)
        Button(plt.axes([hpos_img, vpos_img, 0.02, 0.02]), '', image=dec_img, color='None')
    elif nppings[-1] > avg:
        make_textbox(vpos=vpos_tb, hpos=hpos_tb - 0.05, alpha=a_red, fc="red", ec="black")
        ax1.text(vpos_tb, hpos_tb - 0.05, "Avg: " + format(avg, '.3f') + " ms", transform=ax1.transAxes)
        Button(plt.axes([hpos_img, vpos_img, 0.02, 0.02]), '', image=inc_img, color='None')
    else:
        make_textbox(vpos=vpos_tb, hpos=hpos_tb - 0.05, alpha=a_blue, fc="blue", ec="blue")
        ax1.text(vpos_tb, hpos_tb - 0.05, "Avg: " + format(avg, '.3f') + " ms", transform=ax1.transAxes)
        Button(plt.axes([hpos_img, vpos_img, 0.02, 0.02]), '', image=null_img, color='None')
    # Time data
    make_textbox(vpos=vpos_tb, hpos=hpos_tb - 0.1, alpha=a_blue, fc="blue", ec="blue")
    ax1.text(vpos_tb, hpos_tb-0.1, "Time: " + str(nptimes[-1]) + " s", transform=ax1.transAxes)
    # Maximum Ping data
    make_textbox(vpos=vpos_tb, hpos=hpos_tb - 0.15, alpha=a_blue, fc="blue", ec="blue")
    ax1.text(vpos_tb, hpos_tb-0.15, "Max: " + str(max_ping) + " ms", transform=ax1.transAxes)
    # Minimum Ping data
    make_textbox(vpos=vpos_tb, hpos=hpos_tb - 0.2, alpha=a_blue, fc="blue", ec="blue")
    ax1.text(vpos_tb, hpos_tb-0.2, "Min: " + str(min_ping) + " ms", transform=ax1.transAxes)
    # No. of timeouts
    make_textbox(vpos=vpos_tb, hpos=hpos_tb - 0.25, alpha=a_grey, fc="grey", ec="black")
    ax1.text(vpos_tb, hpos_tb-0.25, "# Timeout: " + str(num_to), transform=ax1.transAxes)
    # No. of unreachables
    make_textbox(vpos=vpos_tb, hpos=hpos_tb - 0.3, alpha=a_grey, fc="grey", ec="black")
    ax1.text(vpos_tb, hpos_tb-0.3, "# Unreachable: " + str(num_un), transform=ax1.transAxes)
    # Shows state of the animated graph
    if state % 2:
        Button(plt.axes([0.8, 0.0225, 0.12, 0.025]), '', image=pl_img, color='None')
    else:
        Button(plt.axes([0.8, 0.0225, 0.12, 0.025]), '', image=pa_img, color='None')
    # Label the axes
    axfont = {'fontname': font}
    ax1.set_ylabel('Ping [ms]', size='large', **axfont)
    ax1.set_xlabel('Time [s]', size='large', **axfont)
    # Title of graph
    ax1.set_title('Ping to League of Legends [' + radio_value + '] Server (' + servers[radio_value] + ')', fontsize=17,
                  fontweight='bold')
    if nppings[-1] > 500:
        ax1.plot(nptimes, gpings, color='g')
        # Draws a yellow graph when ping goes over 200 ms and is less than or equal to 500 ms
        ax1.plot(nptimes, ypings, color='y')
        # Draws a red graph when ping goes over 500 ms
        ax1.plot(nptimes, rpings, color='r', label="Ping")
    elif nppings[-1] > 200:
        ax1.plot(nptimes, gpings, color='g')
        ax1.plot(nptimes, ypings, color='y', label="Ping")
        ax1.plot(nptimes, rpings, color='r')
    else:
        ax1.plot(nptimes, gpings, color='g', label="Ping")
        ax1.plot(nptimes, ypings, color='y')
        ax1.plot(nptimes, rpings, color='r')

    yax_min = ax1.get_ylim()[0]
    yax_max = ax1.get_ylim()[1]
    ax1.set_ylim([yax_min, yax_max])
    ax1.plot(nptimes, nptop, linewidth=0.3, color='r', alpha=0.5)
    ax1.plot(nptimes, npavgs, linewidth=0.3, color='b', label="Average Ping", alpha=0.5)
    ax1.plot(nptimes, npbot, linewidth=0.3, color='c', alpha=0.5)
    ax1.fill_between(nptimes, npbot, nptop, facecolor='blue', interpolate=True, alpha=0.05)
    draw_zones(yax_min, yax_max)
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
    quit_b = Button(plt.axes([0.905, 0.01, 0.089, 0.05]), label='Quit')
    quit_b.on_clicked(ButtonHandler().quit)
    quit_b.label.set_fontsize(15)
    pp_b = Button(plt.axes([0.835, 0.01, 0.1, 0.05]), '', image=pp_img)
    pp_b.on_clicked(ButtonHandler().pause)
    plt.show()

set_savdir()
while nppings.size < 1:
    upd_data()
set_frame()
