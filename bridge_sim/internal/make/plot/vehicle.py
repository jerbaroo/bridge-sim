"""Plots for individual vehicles."""

import matplotlib.pyplot as plt

from bridge_sim.internal.plot.vehicle import topview_vehicle
from bridge_sim.model import Config, Vehicle


def comparison(c: Config, v1: Vehicle, v2: Vehicle):
    """Plot of a vehicle with wheel print compared to with point-loads."""
    plt.landscape()

    wheel_print = (0.31, 0.25)
    wheel_prints = []
    for w_i in range(len(v1.axle_distances) + 1):
        if w_i in [1, 2]:
            wheel_prints.append([wheel_print, wheel_print])
        else:
            wheel_prints.append([wheel_print])

    plt.subplot(1, 2, 1)
    xlim, ylim = topview_vehicle(v1, wheel_prints=wheel_prints)
    plt.title("Truck 1 specification")
    plt.xlabel("Width (m)")
    plt.ylabel("Length (m)")

    plt.subplot(1, 2, 2)
    topview_vehicle(v2, xlim=xlim, ylim=ylim)
    plt.title("Truck 1 in simulation")
    plt.xlabel("Width (m)")
    plt.ylabel("Length (m)")

    plt.savefig(c.get_image_path("vehicles", "wagen-1", bridge=False) + ".pdf")
    plt.close()
