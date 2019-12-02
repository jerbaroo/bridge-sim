"""Plots for individual vehicles."""
import matplotlib.image as mpimg

from classify.vehicle import wagen1
from config import Config
from plot.vehicle import topview_vehicle
from plot import plt


def wagen1_plot(c: Config):
    """Plot of wagen1 compared to given specification."""
    plt.subplot(1, 2, 1)
    img = mpimg.imread("data/vehicle/truck-1.png")
    plt.imshow(img, aspect="auto")
    plt.title("Truck 1 specification")
    plt.xticks([], [])
    plt.yticks([], [])
    plt.xlabel("")
    plt.ylabel("")

    plt.subplot(1, 2, 2)
    topview_vehicle(wagen1)
    plt.title("Truck 1 in simulation")
    plt.xlabel("Width (m)")
    plt.ylabel("Length (m)")

    plt.savefig(c.get_image_path("vehicle", "wagen1", bridge=False))
    plt.close()
