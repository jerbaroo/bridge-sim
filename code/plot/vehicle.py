"""Plot of individual vehicles."""
from itertools import chain

from model.load import Vehicle
from plot import plt
from util import kn_to_kg


def topview_vehicle(vehicle: Vehicle):
    """Plot a vehicle from a top view."""
    axle_y = 0
    kn_per_wheel = list(chain.from_iterable(vehicle.kn_per_wheel()))
    wheel_index = 0
    for axle_delta in [0] + vehicle.axle_distances:
        axle_y -= axle_delta
        y = axle_y + vehicle.length
        plt.plot([0, vehicle.axle_width], [y, y], marker="o", color="black")
        wheel_kn = f"{int(kn_per_wheel[wheel_index] * kn_to_kg)}kN"
        wheel_index += 1
        plt.annotate(wheel_kn, (0, y), (0, y + 0.1))
        wheel_kn = f"{int(kn_per_wheel[wheel_index] * kn_to_kg)}kN"
        wheel_index += 1
        plt.annotate(
            wheel_kn, (vehicle.axle_width, y), (vehicle.axle_width - 0.1, y + 0.1),
        )
