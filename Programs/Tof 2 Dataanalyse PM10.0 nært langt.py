from pylab import *
import numpy as np

close_files = [
    "C:/Users/revil/Desktop/Dataanalyse - AIRBIT/data csv/2026-02-23 RARE MÅLINGER.csv",
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
    all_interp = []
    min_duration = inf

    for file in files:
        # CHANGE HERE → PM10 column (likely 7)
        pm10 = np.genfromtxt(file, skip_header=1, skip_footer=1,
                             usecols=(7,), delimiter=",")

        time_raw = np.genfromtxt(file, skip_header=1, skip_footer=1,
                                 usecols=(1,), delimiter=",", dtype=str)

        seconds = np.array([to_seconds(t) for t in time_raw])
        minutes = (seconds - seconds[0]) / 60

        pm = pm10

        pm_glatt = []
        for j in range(k, len(pm) - k):
            pm_glatt.append(mean(pm[j-k:j+k]))

        minutes_glatt = minutes[k:len(pm)-k]

        # plot individual (faint)
        plot(minutes, pm, color=color, alpha=0.15)
        plot(minutes_glatt, pm_glatt, color=color, alpha=0.5)

        min_duration = minimum(min_duration, minutes_glatt[-1])
        all_interp.append((minutes_glatt, pm_glatt))

    common_minutes = np.linspace(0, min_duration, 500)

    all_values = []
    for minutes_glatt, pm_glatt in all_interp:
        interp = np.interp(common_minutes, minutes_glatt, pm_glatt)
        all_values.append(interp)

    average = np.mean(all_values, axis=0)

    # average line
    plot(common_minutes, average, color=avg_color, linewidth=3,
         linestyle="--", label=f"{group_name} PM10 average")

plot_group(close_files, color="blue", avg_color="darkblue", group_name="Close")
plot_group(far_files,   color="red",  avg_color="darkred",  group_name="Far")

xlabel("Minutes since start")
ylabel("PM10 particle count")
title("PM10 — Close vs Far")
legend()
tight_layout()
show()