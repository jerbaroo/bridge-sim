"""Plot shrinkage over time."""

import matplotlib.pyplot as plt
import numpy as np

from bridge_sim import shrinkage
from bridge_sim.model import Config, Point, RT
from bridge_sim.util import convert_times


def plot_drying_shrinkage(config: Config, n: int = 1):
    """Plot drying shrinkage over n years."""
    days = np.arange(n * 365)
    seconds = convert_times(f="day", t="second", times=days)

    strain = shrinkage.drying(config, shrinkage.CementClass.Normal, seconds)
    plt.plot(days / 365, strain * 1e6, lw=3, c="r")
    plt.ylabel("Microstrain")
    plt.xlabel("Time (years)")
    plt.title(f"Drying shrinkage")
    plt.savefig(config.get_image_path("verification/shrinkage", "drying.pdf"))
    plt.close()

    plt.landscape()
    plt.subplot(2, 1, 1)
    response_type = RT.StrainXXB
    point = Point(x=51)
    responses = shrinkage.drying_responses(
        config=config,
        response_type=response_type,
        times=seconds,
        points=[point],
        cement_class=shrinkage.CementClass.Normal,
    )[0]
    plt.plot(days / 365, responses, lw=3, c="r")
    plt.ylabel("Microstrain XXB")
    plt.tick_params(axis="x", bottom=False, labelbottom=False)

    plt.subplot(2, 1, 2)
    response_type = RT.YTrans
    point = Point(x=51)
    responses = shrinkage.drying_responses(
        config=config,
        response_type=response_type,
        times=seconds,
        points=[point],
        cement_class=shrinkage.CementClass.Normal,
    )[0]
    plt.plot(days / 365, responses * 1e3, lw=3, c="r")
    plt.ylabel(response_type.name() + " (mm)")
    plt.xlabel("Time (years)")
    plt.suptitle(f"Responses to drying shrinkage at X = {point.x} m, Z = {point.z} m")
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(config.get_image_path("verification/shrinkage", "drying-responses.pdf"))
    plt.close()


def plot_autogenous_shrinkage(config: Config, n: int = 1):
    """Plot autogenous shrinkage over n years."""
    days = np.arange(n * 365)
    seconds = convert_times(f="day", t="second", times=days)

    strain = shrinkage.autogenous(seconds)
    plt.plot(days / 365, strain * 1e6, lw=3, c="r")
    plt.ylabel("Microstrain")
    plt.xlabel("Time (years)")
    plt.suptitle(f"Autogenous shrinkage")
    plt.savefig(config.get_image_path("verification/shrinkage", "autogenous.pdf"))
    plt.close()

    plt.landscape()
    plt.subplot(2, 1, 1)
    response_type = RT.StrainXXB
    point = Point(x=51)
    responses = shrinkage.autogenous_responses(
        config=config, response_type=response_type, times=seconds, points=[point],
    )[0]
    plt.plot(days / 365, responses, lw=3, c="r")
    plt.ylabel("Microstrain XXB")
    plt.tick_params(axis="x", bottom=False, labelbottom=False)

    plt.subplot(2, 1, 2)
    response_type = RT.YTrans
    point = Point(x=51)
    responses = shrinkage.autogenous_responses(
        config=config, response_type=response_type, times=seconds, points=[point],
    )[0]
    plt.plot(days / 365, responses * 1e3, lw=3, c="r")
    plt.ylabel(response_type.name() + " (mm)")
    plt.xlabel("Time (years)")
    plt.suptitle(
        f"Responses to autogenous shrinkage at X = {point.x} m, Z = {point.z} m"
    )
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(
        config.get_image_path("verification/shrinkage", "autogenous-responses.pdf")
    )
    plt.close()


def plot_total_shrinkage(config: Config, n: int = 1):
    """Plot total shrinkage over n years."""
    days = np.arange(n * 365)
    seconds = convert_times(f="day", t="second", times=days)

    strain = shrinkage.total(config, shrinkage.CementClass.Normal, seconds)
    plt.plot(days / 365, strain * 1e6, lw=3, c="r")
    plt.ylabel("Microstrain")
    plt.xlabel("Time (years)")
    plt.suptitle(f"Total shrinkage")
    plt.savefig(config.get_image_path("verification/shrinkage", "total.pdf"))
    plt.close()

    plt.landscape()
    plt.subplot(2, 1, 1)
    response_type = RT.StrainXXB
    point = Point(x=51)
    responses = shrinkage.total_responses(
        config=config,
        response_type=response_type,
        times=seconds,
        points=[point],
        cement_class=shrinkage.CementClass.Normal,
    )[0]
    plt.plot(days / 365, responses, lw=3, c="r")
    plt.ylabel("Microstrain XXB")
    plt.tick_params(axis="x", bottom=False, labelbottom=False)

    plt.subplot(2, 1, 2)
    response_type = RT.YTrans
    point = Point(x=51)
    responses = shrinkage.total_responses(
        config=config,
        response_type=response_type,
        times=seconds,
        points=[point],
        cement_class=shrinkage.CementClass.Normal,
    )[0]
    plt.plot(days / 365, responses * 1e3, lw=3, c="r")
    plt.ylabel(response_type.name() + " (mm)")
    plt.xlabel("Time (years)")
    plt.suptitle(f"Responses to total shrinkage at X = {point.x} m, Z = {point.z} m")
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(config.get_image_path("verification/shrinkage", "total-responses.pdf"))
    plt.close()
