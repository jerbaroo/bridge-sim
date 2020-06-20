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

    points = [
        Point(x=x, z=z)
        for x in np.linspace(config.bridge.x_min, config.bridge.x_max, 100)
        for z in np.linspace(config.bridge.z_min, config.bridge.z_max, 100)
    ]
    x = 48
    response_type = ResponseType.StrainXXB
    pier_settlement = PierSettlement(pier=9, settlement=1 / 1e3)
    sw_responses = sim.responses.load(
        config=config, response_type=response_type, self_weight=True,
    )
    ps_responses = sim.responses.load(
        config=config, response_type=response_type, pier_settlement=[pier_settlement],
    )
    sh_responses = shrinkage.total_responses(
        config=config, response_type=response_type, times=seconds, points=points,
    )
    # for responses in
    # creep_responses = creep.creep_responses(
    #     config=config,
    #     times=seconds,
    #     responses=responses,
    #     points=points,
    #     cement_class=shrinkage.CementClass.Normal,
    #     x=x,
    # )

    plt.landscape()
    c = {0: "r", 1: "black", 2: "blue"}
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
                responses = sw_responses
            elif i == 1:
                responses = ps_responses
            elif i == 2:
                responses = shrinkage.total_responses(
                    config=config,
                    response_type=response_type,
                    times=seconds,
                    points=[Point(x=x)],
                )
            creep_responses = creep.creep_responses(
                config=config,
                times=seconds,
                responses=responses,
                points=[Point(x=x)],
                cement_class=shrinkage.CementClass.Normal,
                x=x,
            )[0]
            plt.plot(days / 365, creep_responses, lw=3, c=c[i], label=title)
            plt.xlabel("Time (years)")
            plt.ylabel(
                "Microstrain XXB" if response_type.is_strain() else response_type.name()
            )
        plt.legend()
    plt.suptitle(f"Responses to creep at X = {x} m, Z = {Point().z} m")
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(config.get_image_path("verification/creep", "creep-responses.pdf"))
    plt.close()
