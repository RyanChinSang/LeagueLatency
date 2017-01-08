import subprocess
from datetime import datetime

CREATE_NO_WINDOW = 0x08000000

# This subprocess cannot loop or run indefinitely on its own because of there is no context to logically close it on.

p1 = subprocess.Popen(["ping.exe", "104.160.131.3", "-n", "5", "-l", "500"],
                      stdout=subprocess.PIPE,
                      stdin=subprocess.PIPE,
                      stderr=subprocess.PIPE,
                      shell=False,
                      creationflags=CREATE_NO_WINDOW)

open('values.txt', 'w').close()

lpings = [0]
ltimes = [0]
count = 0
sum_ping = 0
max_ping = 0
min_ping = 9999
start = datetime.now()


for line in iter(p1.stdout.readline, b''):
    if "time=" in line:
        ping = float(line[line.find("time=")+5:line.find("ms")])
        lpings += [ping]
        interval = datetime.now() - start
        ltime = interval.total_seconds()
        ltimes += [ltime]
        sum_ping += ping
        count += 1
        avg_ping = sum_ping/count
        if ping > max_ping:
            max_ping = ping
        if min_ping > ping:
            min_ping = ping

        with open('values.txt', 'a') as values_file:
            values_file.write(str(ltimes[count]) + "," + str(lpings[count]) + "\n")