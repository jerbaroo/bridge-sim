"""Plot of individual vehicles."""
from itertools import chain
from typing import List, Optional, Tuple

from matplotlib.patches import Rectangle

from model.load import Vehicle
from plot import plt
from util import kn_to_kg

# Length and width of a wheel print in meters.
WheelPrint = Tuple[float, float]


def topview_vehicle(
    vehicle: Vehicle,
    wheel_prints: Optional[List[WheelPrint]] = None,
    xlim: Tuple[float, float] = None,
    ylim: Tuple[float, float] = None,
):
    """Plot a vehicle from a top view."""
    axle_y = 0
    wheel_index = 0
    kn_per_wheel = list(chain.from_iterable(vehicle.kn_per_wheel()))
    for a_i, axle_delta in enumerate([0] + vehicle.axle_distances):
        # Determine wheel print dimensions for the current axle.
        if wheel_prints is not None:
            half_wheel_length = wheel_prints[a_i][0] / 2
            half_wheel_width = wheel_prints[a_i][1] / 2
            print(half_wheel_width, half_wheel_length)

        # Plot the current axle.
        axle_y -= axle_delta
        y = axle_y + vehicle.length
        if wheel_prints is None:
            plt.plot([0, vehicle.axle_width], [y, y], marker="o", color="black")
        else:
            plt.plot(
                [0 + half_wheel_width, vehicle.axle_width - half_wheel_width],
                [y, y],
                color="black",
            )

        # Annotate one wheel with load intensity.
        wheel_kn = f"{int(kn_per_wheel[wheel_index] * kn_to_kg)} kN"
        wheel_index += 1
        plt.annotate(wheel_kn, (0, y), (0, y + 0.25))
        if wheel_prints is not None:
            plt.gca().add_patch(
                Rectangle(
                    (0 - half_wheel_width, y - half_wheel_length),
                    wheel_prints[a_i][1],
                    wheel_prints[a_i][0],
                    facecolor="none",
                    edgecolor="black",
                )
            )

        # Annotate the other wheel with load intensity.
        wheel_kn = f"{int(kn_per_wheel[wheel_index] * kn_to_kg)} kN"
        wheel_index += 1
        plt.annotate(
            wheel_kn, (vehicle.axle_width, y), (vehicle.axle_width - 1, y + 0.25)
        )
        if wheel_prints is not None:
            plt.gca().add_patch(
                Rectangle(
                    (vehicle.axle_width - half_wheel_width, y - half_wheel_length),
                    wheel_prints[a_i][1],
                    wheel_prints[a_i][0],
                    facecolor="none",
                    edgecolor="black",
                )
            )

    plt.axis("equal")
    if xlim is not None:
        plt.xlim(xlim)
    if ylim is not None:
        plt.ylim(ylim)
    return plt.xlim(), plt.ylim()
