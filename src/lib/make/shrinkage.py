import matplotlib.pyplot as plt
import numpy as np

from bridge_sim import shrinkage


def plot_drying_shrinkage():
    days = np.arange(1 * 365)
    strain = shrinkage.drying(shrinkage.CementClass.Normal, 250, days)
    plt.plot(days / 365, strain * 1E6, lw=3, c="r")
    plt.ylim(plt.ylim()[1] / 10, plt.ylim()[1])
    plt.ylabel("Microstrain")
    plt.xlabel("Time (years)")
    plt.title("Drying shrinkage")
    plt.tight_layout()
    plt.show()


def plot_autogenous_shrinkage():
    days = np.arange(1 * 365)
    strain = shrinkage.autogenous(days)
    plt.plot(days / 365, strain * 1E6, lw=3, c="r")
    plt.ylim(plt.ylim()[1] / 10, plt.ylim()[1])
    plt.ylabel("Microstrain")
    plt.xlabel("Time (years)")
    plt.title("Autogenous shrinkage")
    plt.tight_layout()
    plt.show()
