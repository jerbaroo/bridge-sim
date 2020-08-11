"""Plot creep over time."""

import matplotlib.pyplot as plt
import numpy as np

from bridge_sim import creep, shrinkage, sim
from bridge_sim.model import Config, Point, RT, ResponseType, PierSettlement
from bridge_sim.util import convert_times


def plot_creep(config: Config, x: float, z: float, n: int = 100):
    """Plot creep over n years."""
    days = np.arange(n * 365)
    seconds = convert_times(f="day", t="second", times=days)

    strain = creep.creep_coeff(config, shrinkage.CementClass.Normal, seconds, 51)
    for s in strain:
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
    point = Point(x=x, z=z)
    install_day, start_day, end_day, signal_len = 37, 37, 100 * 365, 100
    for r_i, response_type in enumerate([ResponseType.YTrans, ResponseType.StrainXXB]):
        plt.subplot(1, 2, r_i + 1)
        pier_settlement = PierSettlement(pier=5, settlement=1 / 1e3)
        for i, (name, sw, ps, sh, c) in enumerate(
            [
                ["self-weight", True, [], False, "black"],
                [
                    "pier settlement",
                    False,
                    [(pier_settlement, pier_settlement)],
                    False,
                    "blue",
                ],
                ["shrinkage", False, [], True, "red"],
            ]
        ):
            creep_responses = sim.responses.to_creep(
                config=config,
                points=[point],
                responses_array=np.empty((1, signal_len)),
                response_type=response_type,
                install_day=install_day,
                start_day=start_day,
                end_day=end_day,
                self_weight=sw,
                pier_settlement=ps,
                shrinkage=sh,
            )[0]
            xs = (
                np.interp(
                    np.arange(len(creep_responses)),
                    [0, len(creep_responses) - 1],
                    [start_day, end_day],
                )
                / 365
            )
            if response_type.is_strain():
                plt.semilogy(xs, creep_responses * 1e6, label=name, lw=3, c=c)
            else:
                plt.plot(xs, creep_responses * 1e3, label=name, lw=3, c=c)
            plt.ylabel(
                "Microstrain XXB" if response_type.is_strain() else "Y translation (mm)"
            )
            plt.xlabel("Time (years)")
        plt.legend()
    plt.suptitle(f"Responses to creep at X = {point.x} m, Z = {point.z} m")
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(config.get_image_path("verification/creep", "creep-responses.pdf"))
    plt.close()
