"""Plots for individual vehicles."""
import matplotlib.image as mpimg

from classify.vehicle import wagen1
from config import Config
from plot.vehicle import topview_vehicle
from plot import plt


def wagen1_plot(c: Config):
    """Plot of wagen1 compared to given specification."""
    plt.landscape()

    plt.subplot(1, 2, 1)
    xlim, ylim = topview_vehicle(wagen1, wheel_print=(0.31, 0.25))
    plt.title("Truck 1 specification")
    plt.xlabel("Width (m)")
    plt.ylabel("Length (m)")

    plt.subplot(1, 2, 2)
    topview_vehicle(wagen1, xlim=xlim, ylim=ylim)
    plt.title("Truck 1 in simulation")
    plt.xlabel("Width (m)")
    plt.ylabel("Length (m)")

    plt.savefig(c.get_image_path("vehicle", "wagen-1", bridge=False) + ".pdf")
    plt.close()
