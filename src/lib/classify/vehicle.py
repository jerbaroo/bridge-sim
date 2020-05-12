import pandas as pd

from lib.model.load import MvVehicle
from util import kg_to_kn

# Wagen 1 from the experimental campaign.
wagen1 = MvVehicle(
    kn=[
        (5050 * kg_to_kn, 5300 * kg_to_kn),
        (4600 * kg_to_kn, 4000 * kg_to_kn),
        (4350 * kg_to_kn, 3700 * kg_to_kn),
        (4050 * kg_to_kn, 3900 * kg_to_kn),
    ],
    axle_distances=[3.6, 1.32, 1.45],
    axle_width=2.5,
    # In dynamic test 'D1a' the speed was 20 kmph.
    kmph=20,
    lane=0,
    init_x_frac=0,
)


def wagen1_x_pos():
    """X positions of the front of Truck 1 in the experimental campaign."""
    meas = pd.read_csv("data/verification/measurements_static_ZB.csv")
    return sorted(set(meas["xpostruck"]))
