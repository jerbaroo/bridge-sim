import os

import numpy as np
from scipy.signal import savgol_filter

temperatures = dict()


def load_temperature_month(month: str):
    if month in temperatures:
        return temperatures[month]
    def parse_line(line):
        line = line.split()
        try:
            return float(line[1][-4:]), float(line[-1])
        except:
            return str, np.nan
    with open(os.path.join("data/temperature", month + ".txt")) as f:
        temperatures[month] = list(map(parse_line, f.readlines()))
    # Remove NANs.
    for line_ind, (time, temp) in enumerate(temperatures[month]):
        if np.isnan(temp):
            print_i(f"NAN in {month} temperature")
            temperatures[month][line_ind] = (time, temperatures[month][line_ind - 1])
    # Unpack.
    time, temperature = (
        np.array([l[0] for l in temperatures[month]]),
        np.array([l[1] for l in temperatures[month]]),
    )
    # Convert to celcius.
    temperature = (temperature - 32) * (5 / 9)
    # Regularize time.
    # Smooth.
    temperature = savgol_filter(temperature, 51, 3) # window size 51, polynomial order 3
    # Save.
    temperatures[month] = (time, temperature)
    return temperatures[month]


def temperature_effect(response_type: ResponseType):
