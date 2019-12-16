"""Plot of individual vehicles."""
from itertools import chain
from typing import Optional, Tuple

from matplotlib.patches import Rectangle

from model.load import Vehicle
from plot import plt
from util import kn_to_kg


def topview_vehicle(
        vehicle: Vehicle,
        wheel_print: Optional[Tuple[float, float]] = None,
        xlim: Tuple[float, float] = None,
        ylim: Tuple[float, float] = None,
):
    """Plot a vehicle from a top view."""
    if wheel_print is not None:
        half_wheel_width = wheel_print[1] / 2
        half_wheel_length = wheel_print[0] / 2
        print(half_wheel_width, half_wheel_length)

    axle_y = 0
    wheel_index = 0
    kn_per_wheel = list(chain.from_iterable(vehicle.kn_per_wheel()))
    for axle_delta in [0] + vehicle.axle_distances:
        # Plot the axle.
        axle_y -= axle_delta
        y = axle_y + vehicle.length
        if wheel_print is None:
            plt.plot([0, vehicle.axle_width], [y, y], marker="o", color="black")
        else:
            plt.plot([0 + half_wheel_width, vehicle.axle_width - half_wheel_width], [y, y], color="black")

        # Annotate one wheel with load intensity.
        wheel_kn = f"{int(kn_per_wheel[wheel_index] * kn_to_kg)} kN"
        wheel_index += 1
        plt.annotate(wheel_kn, (0, y), (0, y + 0.25))
        if wheel_print is not None:
            plt.gca().add_patch(Rectangle(
                (0 - half_wheel_width, y - half_wheel_length),
                wheel_print[1],
                wheel_print[0],
                facecolor="none",
                edgecolor="black",
            ))


        # Annotate the other wheel with load intensity.
        wheel_kn = f"{int(kn_per_wheel[wheel_index] * kn_to_kg)} kN"
        wheel_index += 1
        plt.annotate(wheel_kn, (vehicle.axle_width, y), (vehicle.axle_width - 1, y + 0.25))
        if wheel_print is not None:
            plt.gca().add_patch(Rectangle(
                (vehicle.axle_width - half_wheel_width, y - half_wheel_length),
                wheel_print[1],
                wheel_print[0],
                facecolor="none",
                edgecolor="black",
            ))

    plt.axis("equal")
    if xlim is not None:
        plt.xlim(xlim)
    if ylim is not None:
        plt.ylim(ylim)
    return plt.xlim(), plt.ylim()
