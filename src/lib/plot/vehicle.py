"""Plot of individual vehicles."""

from itertools import chain
from typing import List, Optional, Tuple

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from bridge_sim.model import Vehicle
from bridge_sim.util import kn_to_kg

# Length and width of a wheel print in meters.
WheelPrint = Tuple[float, float]


def topview_vehicle(
    vehicle: Vehicle,
    wheel_prints: Optional[List[List[WheelPrint]]] = None,
    xlim: Tuple[float, float] = None,
    ylim: Tuple[float, float] = None,
):
    """Plot a single "Vehicle" from a top view."""
    if isinstance(vehicle.load, list) and isinstance(vehicle.load[0], list):
        kn_per_wheel = vehicle.load
    else:
        print(vehicle.load_per_axle())
        kn_per_wheel = [[kn / 2, kn / 2] for kn in vehicle.load_per_axle()]
    kn_per_wheel = list(chain.from_iterable(kn_per_wheel))

    axle_y = 0
    wheel_index = 0
    for a_i, axle_delta in enumerate([0] + vehicle.axle_distances):
        # Determine wheel print dimensions for the current axle.
        if wheel_prints is not None:
            wheel_lengths = list(map(lambda wp: wp[0], wheel_prints[a_i]))
            wheel_widths = list(map(lambda wp: wp[1], wheel_prints[a_i]))
            wheels_length = sum(wheel_lengths)
            wheels_width = sum(wheel_widths)
            half_wheels_length = wheels_length / 2
            half_wheels_width = wheels_width / 2

        # Plot the current axle.
        axle_y -= axle_delta
        y = axle_y + vehicle.length
        if wheel_prints is None:
            plt.plot([0, vehicle.axle_width], [y, y], marker="o", color="black")
        else:
            plt.plot(
                [0 + half_wheels_width, vehicle.axle_width - half_wheels_width],
                [y, y],
                color="black",
            )

        # Annotate left-axle wheel with load intensity.
        wheel_kn = f"{int(kn_per_wheel[wheel_index] * kn_to_kg)} kN"
        wheel_index += 1
        plt.annotate(wheel_kn, (0, y), (0, y + 0.25))
        if wheel_prints is not None:
            left = 0 + half_wheels_width
            for wheel_print in wheel_prints[a_i]:
                left -= wheel_print[1]
                bottom = y - (wheel_print[0] / 2)
                plt.gca().add_patch(
                    Rectangle(
                        (left, bottom),
                        wheel_print[1],
                        wheel_print[0],
                        facecolor="none",
                        edgecolor="black",
                    )
                )

        # Annotate right-axle wheel with load intensity.
        wheel_kn = f"{int(kn_per_wheel[wheel_index] * kn_to_kg)} kN"
        wheel_index += 1
        plt.annotate(
            wheel_kn, (vehicle.axle_width, y), (vehicle.axle_width - 1, y + 0.25)
        )
        if wheel_prints is not None:
            left = vehicle.axle_width - half_wheels_width
            for wheel_print in wheel_prints[a_i]:
                bottom = y - (wheel_print[0] / 2)
                plt.gca().add_patch(
                    Rectangle(
                        (left, bottom),
                        wheel_print[1],
                        wheel_print[0],
                        facecolor="none",
                        edgecolor="black",
                    )
                )
                left += wheel_print[1]

    plt.axis("equal")
    if xlim is not None:
        plt.xlim(xlim)
    if ylim is not None:
        plt.ylim(ylim)
    return plt.xlim(), plt.ylim()
