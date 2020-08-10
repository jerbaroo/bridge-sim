import numpy as np

from bridge_sim.plot import plt


def plot_day_lines(datetimes):
    """Plot a vertical line every 00:00. You still have to call plt.legend."""
    label_set = False
    for dt in datetimes:
        if np.isclose(float(dt.hour + dt.minute), 0):
            label = None
            if not label_set:
                label = "Time = 00:00"
                label_set = True
            plt.axvline(x=dt, linewidth=1, color="black", label=label)
