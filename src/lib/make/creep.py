"""Plot creep over time."""

import matplotlib.pyplot as plt
import numpy as np

from bridge_sim import creep, shrinkage, sim, plot
from bridge_sim.model import Config, Point, RT, ResponseType, PierSettlement
from bridge_sim.util import convert_times


def plot_creep(config: Config, n: int = 100):
    """Plot creep over n years."""
    days = np.arange(n * 365)
    seconds = convert_times(f="day", t="second", times=days)

    strain = creep.creep_coeff(config, shrinkage.CementClass.Normal, seconds, 51)
    for s in strain:
        print(s)
        if not np.isnan(s):
            break
    plt.plot(days / 365, strain, lw=3, c="r")
    plt.ylabel("Creep coefficient")
    plt.xlabel("Time (years)")
    plt.title(f"Creep")
    plt.tight_layout()
    plt.savefig(config.get_image_path("verification/creep", "creep_coeff.pdf"))
    plt.close()

    plt.landscape()
    point = Point(x=48)
    pier_settlement = PierSettlement(pier=9, settlement=1)
    c = {0: "r", 1: "g", 2: "b"}
    for r_i, response_type in enumerate([RT.StrainXXB, RT.YTrans]):
        for i, title in enumerate(
            [
                "Self-weight",
                f"{pier_settlement.settlement} mm settlement of pier {pier_settlement.pier}",
                "Shrinkage",
            ]
        ):
            plt.subplot(2, 1, r_i + 1)
            if i == 0:
                responses = sim.responses.load(
                    config=config, response_type=response_type, self_weight=True,
                )
                if not response_type.is_strain():
                    responses = responses.map(lambda r: r * 1e3)
            elif i == 1:
                responses = sim.responses.load(
                    config=config,
                    response_type=response_type,
                    pier_settlement=[pier_settlement],
                )
            elif i == 2:
                responses = shrinkage.total_responses(
                    config=config,
                    response_type=response_type,
                    times=seconds,
                    points=[point],
                )
                if not response_type.is_strain():
                    responses *= 1e3
            creep_responses = creep.creep_responses(
                config=config,
                times=seconds,
                responses=responses,
                points=[point],
                cement_class=shrinkage.CementClass.Normal,
                x=51,
            )[0]
            plt.plot(days / 365, creep_responses, lw=3, c=c[i], label=title)
            plt.xlabel("Time (years)")
            plt.ylabel(
                "Microstrain XXB" if response_type.is_strain() else response_type.name()
            )
        plt.legend()
    plt.suptitle(f"Responses to creep at X = {point.x} m, Z = {point.z} m")
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(config.get_image_path("verification/creep", "creep-responses.pdf"))
    plt.close()
