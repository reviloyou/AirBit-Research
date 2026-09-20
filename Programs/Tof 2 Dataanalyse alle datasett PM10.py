from pylab import *
import numpy as np

# Files go here with a , after and then enter to go down
close_files = [
    
]

far_files = [
    
]

def to_seconds(t):
    h, m, s = t.split(":")
    return int(h) * 3600 + int(m) * 60 + int(s)

k = 5

def plot_group(files, color, group_name):
    for file in files:
        hopen = np.genfromtxt(file, skip_header=1, skip_footer=1,
                              usecols=(7,), delimiter=",")
        time_raw = np.genfromtxt(file, skip_header=1, skip_footer=1,
                                  usecols=(1,), delimiter=",", dtype=str)

        seconds = np.array([to_seconds(t) for t in time_raw])
        minutes = (seconds - seconds[0]) / 60

        pm10 = hopen
        pm10_glatt = []
        for j in range(k, len(pm10) - k):
            pm10_glatt.append(mean(pm10[j-k:j+k]))

        date = file.split("/")[-1].replace(".csv", "")
        label = f"{group_name} — {date}"

        plot(minutes, pm10, color=color, alpha=0.15)
        plot(minutes[k:len(pm10)-k], pm10_glatt, color=color, label=label)

plot_group(close_files, color="blue", group_name="close")
plot_group(far_files,   color="red",  group_name="far")

xlabel("Minutes since start")
ylabel("Particle count")
title("PM10 — Close vs Far")
legend()
tight_layout()
show()