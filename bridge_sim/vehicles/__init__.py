"""Provided instances of the Vehicle class."""

from bridge_sim.model import Vehicle
from bridge_sim.util import kg_to_kn

truck1 = Vehicle(
    load=[
        ((5050 + 5300) * kg_to_kn * 1e3),
        ((4600 + 4000) * kg_to_kn * 1e3),
        ((4350 + 3700) * kg_to_kn * 1e3),
        ((4050 + 3900) * kg_to_kn * 1e3),
    ],
    axle_distances=[3.6, 1.32, 1.45],
    axle_width=2.5,
    # In dynamic test 'D1a' the speed was 20 kmph.
    kmph=20,
)
"""Truck 1 from the experimental campaign."""

og_truck1 = Vehicle(
    load=[
        [5050 * kg_to_kn * 1e3, 5300 * kg_to_kn * 1e3],
        [4600 * kg_to_kn * 1e3, 4000 * kg_to_kn * 1e3],
        [4350 * kg_to_kn * 1e3, 3700 * kg_to_kn * 1e3],
        [4050 * kg_to_kn * 1e3, 3900 * kg_to_kn * 1e3],
    ],
    axle_distances=[3.6, 1.32, 1.45],
    axle_width=2.5,
    # In dynamic test 'D1a' the speed was 20 kmph.
    kmph=20,
)
"""Truck 1 from the experimental campaign with a load per wheel."""

assert og_truck1.lane == 0
assert og_truck1.init_x == 0

__all__ = ["truck1"]
