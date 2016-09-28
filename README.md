# League Latency

A Graphical UI that provides real-time Statistics and Graphs about your ping (latency) to the League of Legends NA or LAN server.

## How to Install
League Latency is currently not ported to a Windows .exe just yet... but, it soon will!
In the meanwhile we will need to follow a "much-longer-than-I-want-to-have" installation process.
It is still simple! But not simple for everyone.

### Step 1: Get Python

####1. Find out your Windows version (64-bit or 32-bit) [here](https://support.microsoft.com/en-us/help/13443/windows-which-operating-system).

####2. Download [Python](https://www.python.org/):
1. If you are on 64-bit Windows, download the latest Python 2.7 installer [here](https://www.python.org/ftp/python/2.7.12/python-2.7.12.amd64.msi).
2. If you are on 32-bit Windows, download the latest Python 2.7 installer [here](https://www.python.org/ftp/python/2.7.12/python-2.7.12.msi).

####3. Install Python:
1. Run the installer when download completes.
    1. During installation:
        1. If the **Open File - Security Warning** window pops-up, click **Run**.
        2. Verify you selected **Install for all users**, click **Next**.
        3. Verify that under **Select Destination Directory** the directory stated is `C:\Python27\`, click **Next**.
        4. Under **Customize Python 2.7.12**.
            1. Scroll down to **Add python.exe to Path**.
            2. Click the red 'x' and select **Will be installed on local hard drive**.
            3. Click **Next**.
2. If you did not **Add python.exe to Path** during installation:
    1. Hold <kbd>Win</kbd> and press <kbd>R</kbd>.
    2. Type `explorer` and press <kbd>Enter</kbd>.
    3. Right-click **Computer** or **My Computer** or **This PC** in the <u>Navigation Tree Panel</u> on the left.
    4. Select **Properties** at the bottom of the Context Menu.
    5. Select **Advanced system settings**.
    6. Click **Environment Variables...** in the Advanced Tab.
    7. Under 'System Variables':
        1. Add
            * PY_HOME
            `C:\Python27`
            * PYTHONPATH
            `%PY_HOME%\Lib;%PY_HOME%\DLLs;%PY_HOME%\Lib\lib-tk;C:\another-library`
        2. Append
            * Path
            `%PY_HOME%;%PY_HOME%\Scripts\`
3. **If your main drive is not `C:\`, then replace all occurrences above with your [drive letter](http://www.sevenforums.com/tutorials/82994-drive-letter-add-change-remove-windows.html).**

####4. Verify that python was installed properly.
1. Hold <kbd>Win</kbd> and press <kbd>R</kbd>.
2. Type `cmd` and press <kbd>Enter</kbd>.
3. Type `python` and press <kbd>Enter</kbd>.
    1. If the message is <u>similar</u> to:
    `Python 2.7.12 (v2.7.12:d33e0cf91556, Jun 27 2016, 15:24:40) [MSC v.1500 64 bit (AMD64)] on win32
    Type "help", "copyright", "credits" or "license" for more information.`
    then, congratulations!
    2. If the message is:
    `'python' is not recognized as an internal or external command, operable program or batch file.﻿`
    then, go to **Step 1: 3. 2.**

### Step 2: Get the dependencies
1. Hold <kbd>Win</kbd> and press <kbd>R</kbd>.
2. Type `cmd` and press <kbd>Enter</kbd>.
3. Type `python -m pip install matplotlib` and press <kbd>Enter</kbd>.
    1. If you receive a message with `Successfully installed ...` in it, then congratulations!
    2. If any errors have occurred, you may have a deeper problem. Try a Google search for your received error message and see if there are any solutions, or contact me.

### Step 3: Get League Latency
1. Go [here](https://github.com/RyanChinSang/LeagueLatency/raw/master/History/v2.1c%20Stable.zip) to download the latest, Stable LL (v2.1c)
2. Unzip the files to wherever you'd like.
3. Double-click `LL.py`.

## About
* **Bio**: My name is `Ryan Kevin Chin Sang`. I am a 3rd Year student at the [Univeristy of the West Indies, St. Augustine, Trinidad](http://sta.uwi.edu/) currently pursuing a **BSc. Electrical and Computer Engineering** focusing on the Communications and Computers thematic double-major. As I am a 'college' student, my free-time is very limited. As it stands, my time is always split squarely between Schoolwork (studying, doing assignments/labs, researching) and 'Me'-time (playing League of Legends, spending time with the gf, house-hold duties, etc.). The time I can spend on developing LeagueLatency is very small... but I love developing and I make sure to spend a fair amount of time on it, anyway.
* **Contact**:
    * Email: `ryancs1995@gmail.com`
    * Facebook: [Ryan Chin Sang](https://www.facebook.com/RyanCS1995)
