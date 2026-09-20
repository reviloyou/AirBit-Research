from pylab import *
import numpy as np

hopen = np.genfromtxt("C:/Users/revil/Desktop/Dataanalyse - AIRBIT/data csv/2026-02-16.csv",
                skip_header=1, skip_footer=1,
                usecols=(7,), delimiter=",")

time_raw = np.genfromtxt("C:/Users/revil/Desktop/Dataanalyse - AIRBIT/data csv/2026-02-16.csv",
                          skip_header=1, skip_footer=1,
                          usecols=(1,), delimiter=",", dtype=str)

def to_seconds(t):
    h, m, s = t.split(":")
    return int(h) * 3600 + int(m) * 60 + int(s)

seconds = np.array([to_seconds(t) for t in time_raw])
minutes = (seconds - seconds[0]) / 60

pm10 = hopen

k = 5
pm10_glatt = []
for i in range(k, len(pm10) - k):
    pm10_glatt.append(mean(pm10[i-k:i+k]))

plot(minutes, pm10, color="red", alpha=0.3)
plot(minutes[k:len(pm10)-k], pm10_glatt, color="red", label="PM10")
xlabel("Minutes since start")
ylabel("Particle count")
title("PM10 Particle Count over Time")
legend()
tight_layout()
show()