from pylab import *
import numpy as np

close_files = [
    "C:/Users/revil/Desktop/Dataanalyse - AIRBIT/data csv/2026-02-25.csv",
    "C:/Users/revil/Desktop/Dataanalyse - AIRBIT/data csv/2026-03-02.csv",
    "C:/Users/revil/Desktop/Dataanalyse - AIRBIT/data csv/2026-03-09.csv",
    "C:/Users/revil/Desktop/Dataanalyse - AIRBIT/data csv/2026-03-12.csv",
    "C:/Users/revil/Desktop/Dataanalyse - AIRBIT/data csv/2026-03-17.csv",
    "C:/Users/revil/Desktop/Dataanalyse - AIRBIT/data csv/2026-03-24.csv",
]

far_files = [
    "C:/Users/revil/Desktop/Dataanalyse - AIRBIT/data csv/2026-02-16.csv",
    "C:/Users/revil/Desktop/Dataanalyse - AIRBIT/data csv/2026-02-17.csv",
    "C:/Users/revil/Desktop/Dataanalyse - AIRBIT/data csv/2026-02-24.csv",
    "C:/Users/revil/Desktop/Dataanalyse - AIRBIT/data csv/2026-02-27.csv",
    "C:/Users/revil/Desktop/Dataanalyse - AIRBIT/data csv/2026-03-03.csv",
    "C:/Users/revil/Desktop/Dataanalyse - AIRBIT/data csv/2026-03-10.csv",
    "C:/Users/revil/Desktop/Dataanalyse - AIRBIT/data csv/2026-03-18.csv",
    "C:/Users/revil/Desktop/Dataanalyse - AIRBIT/data csv/2026-03-23.csv",
]

def to_seconds(t):
    h, m, s = t.split(":")
    return int(h) * 3600 + int(m) * 60 + int(s)

k = 5

def plot_group(files, color, avg_color, group_name):
    all_interp = []       # stores each recording interpolated onto common grid
    min_duration = inf    # finds the shortest recording length

    # First pass — plot individual lines and find shortest duration
    for file in files:
        hopen = np.genfromtxt(file, skip_header=1, skip_footer=1,
                              usecols=(6,), delimiter=",")
        time_raw = np.genfromtxt(file, skip_header=1, skip_footer=1,
                                  usecols=(1,), delimiter=",", dtype=str)

        seconds = np.array([to_seconds(t) for t in time_raw])
        minutes = (seconds - seconds[0]) / 60

        pm25 = hopen
        pm25_glatt = []
        for j in range(k, len(pm25) - k):
            pm25_glatt.append(mean(pm25[j-k:j+k]))

        # Minutes axis matching the smoothed data
        minutes_glatt = minutes[k:len(pm25)-k]

        date = file.split("/")[-1].replace(".csv", "")
        label = f"{group_name} — {date}"

        plot(minutes, pm25, color=color, alpha=0.15)
        plot(minutes_glatt, pm25_glatt, color=color, alpha=0.5, label=label)

        # Track shortest duration and store for averaging
        min_duration = minimum(min_duration, minutes_glatt[-1])
        all_interp.append((minutes_glatt, pm25_glatt))

    # Second pass — interpolate all onto common grid and average
    common_minutes = np.linspace(0, min_duration, 500)
    all_values = []
    for minutes_glatt, pm25_glatt in all_interp:
        interp = np.interp(common_minutes, minutes_glatt, pm25_glatt)
        all_values.append(interp)

    average = np.mean(all_values, axis=0)

    # Plot average as thick line
    plot(common_minutes, average, color=avg_color, linewidth=3,
         linestyle="--", label=f"{group_name} AVERAGE")

plot_group(close_files, color="blue", avg_color="darkblue",  group_name="close")
plot_group(far_files,   color="red",  avg_color="darkred",   group_name="far")

xlabel("Minutes since start")
ylabel("Particle count")
title("PM2.5 — Close vs Far")
legend()
tight_layout()
show()