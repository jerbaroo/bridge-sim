"""Plot shrinkage over time."""

import matplotlib.pyplot as plt
import numpy as np

from bridge_sim import plot, shrinkage
from bridge_sim.model import Config, Point, RT
from bridge_sim.util import convert_times


def plot_shrinkage_strain(config: Config, n: int = 100, x: float = 51):
    """Plot shrinkage strain over n years."""
    days = np.arange(n * 365)
    seconds = convert_times(f="day", t="second", times=days)

    E_ca = shrinkage.autogenous(seconds)
    E_cd = shrinkage.drying(config, shrinkage.CementClass.Normal, seconds, x=x)
    E_cs = shrinkage.total(config, shrinkage.CementClass.Normal, seconds, x=x)

    plt.landscape()
    plt.subplot(1, 3, 1)
    plt.plot(days / 365, E_ca * 1e6, lw=3, c="r")
    plt.ylabel("Microstrain")
    plt.xlabel("Time (years)")
    plt.title(f"Autogenous shrinkage")
    plt.subplot(1, 3, 2)
    plt.plot(days / 365, E_cd * 1e6, lw=3, c="r")
    plt.xlabel("Time (years)")
    plt.title(f"Drying shrinkage")
    plt.tick_params(axis="y", left=False, labelleft=False)
    plt.subplot(1, 3, 3)
    plt.plot(days / 365, E_cs * 1e6, lw=3, c="r")
    plt.xlabel("Time (years)")
    plt.title(f"Total shrinkage")
    plt.tick_params(axis="y", left=False, labelleft=False)
    plot.util.equal_lims("y", 1, 3)
    plt.savefig(config.get_image_path("verification/shrinkage", "strain.pdf"))
    plt.close()


def plot_shrinkage_responses(config: Config, n: int = 100, x: float = 51, z: float = 0):
    """Plot shrinkage responses over n years."""
    days = np.arange(n * 365)
    seconds = convert_times(f="day", t="second", times=days)
    response_types = [RT.YTrans, RT.StrainXXB]
    plt.landscape()
    for r_i, rt in enumerate(response_types):
        plt.subplot(1, 2, r_i + 1)
        lw = 3
        drying = shrinkage.drying_responses(
            config=config,
            response_type=rt,
            times=seconds,
            points=[Point(x=x)],
            cement_class=shrinkage.CementClass.Normal,
            x=x,
        )[0] * (1e6 if rt.is_strain() else 1e3)
        plt.plot(days / 365, drying, lw=lw, c="black", label="drying")
        autogenous = shrinkage.autogenous_responses(
            config=config, response_type=rt, times=seconds, points=[Point(x=x)],
        )[0] * (1e6 if rt.is_strain() else 1e3)
        plt.plot(days / 365, autogenous, lw=lw, c="blue", label="autogenous")
        total = shrinkage.total_responses(
            config=config,
            response_type=rt,
            times=seconds,
            points=[Point(x=x)],
            cement_class=shrinkage.CementClass.Normal,
            x=x,
        )[0] * (1e6 if rt.is_strain() else 1e3)
        plt.plot(days / 365, total, lw=lw, c="r", label="total")
        plt.xlabel("Time (years)")
        plt.ylabel("Microstrain XXB" if rt.is_strain() else f"{rt.name()} (mm)")
        plt.legend()
    plt.suptitle(f"Responses at X = {x} m, Z = {z} m from shrinkage")
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(config.get_image_path("verification/shrinkage", "responses.pdf"))
    plt.close()
