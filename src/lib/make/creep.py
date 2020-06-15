"""Plot creep over time."""

import matplotlib.pyplot as plt
import numpy as np

from bridge_sim import creep, shrinkage
from bridge_sim.model import Config, Point, RT
from bridge_sim.util import convert_times


def plot_creep(config: Config, n: int = 100):
    """Plot creep over n years."""
    days = np.arange(n * 365)
    seconds = convert_times(f="day", t="second", times=days)

    strain = creep.creep(shrinkage.CementClass.Normal, 250, seconds)
    for s in strain:
        print(s)
        if not np.isnan(s):
            break
    plt.plot(days / 365, strain, lw=3, c="r")
    plt.ylabel("Creep coefficient")
    plt.xlabel("Time (years)")
    plt.title(f"Creep")
    plt.savefig(config.get_image_path("verification/creep", "creep.pdf"))
    plt.close()

    plt.landscape()
    plt.subplot(2, 1, 1)
    response_type = RT.StrainXXB
    point = Point(x=51)
    responses = creep.creep_responses(
        config=config,
        response_type=response_type,
        times=seconds,
        points=[point],
        cement_class=shrinkage.CementClass.Normal,
        h_0=250,
    )[0]
    plt.plot(days / 365, responses * 1e-6, lw=3, c="r")
    plt.ylabel("Microstrain XXB")
    plt.tick_params(axis="x", bottom=False, labelbottom=False)

    plt.subplot(2, 1, 2)
    response_type = RT.YTrans
    point = Point(x=51)
    responses = creep.creep_responses(
        config=config,
        response_type=response_type,
        times=seconds,
        points=[point],
        cement_class=shrinkage.CementClass.Normal,
        h_0=250,
    )[0]
    plt.plot(days / 365, responses * 1e-3, lw=3, c="r")
    plt.ylabel(response_type.name() + " (mm)")
    plt.xlabel("Time (years)")
    plt.suptitle(f"Responses to creep at X = {point.x} m, Z = {point.z} m")
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(config.get_image_path("verification/creep", "creep-responses.pdf"))
    plt.close()

