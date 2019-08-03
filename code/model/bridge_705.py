"""Model and configuration for bridge 705 in Amsterdam."""
from config import Config
from model import *


def bridge_705_config() -> Config:
    return Config(
        bridge_705,
        vehicle_data_path="data/a16-data/a16.csv",
        vehicle_density=[
            # (2.4, 0.7), (5.6, 90.1), (11.5, 5.9), (12.2, 0.3), (43, 0.1)],
            (11.5, 5.9), (12.2, 0.3), (43, 0.1)],
        vehicle_intensity=None)


# TODO: Make into a reusable function.
def bridge_705() -> Bridge:

    _bridge_705_piers = [0]  # Pier locations in meters.
    for span_distance in [12.75, 15.30, 15.30, 15.30, 15.30, 15.30, 12.75]:
        _bridge_705_piers.append(_bridge_705_piers[-1] + span_distance)
    _bridge_705_length = 102
    fixed_nodes = [Fix(x / _bridge_705_length, y=True)
                   for x in _bridge_705_piers]
    fixed_nodes[0].x = True

    return Bridge(
        name="Bridge 705",
        length=_bridge_705_length,
        width=33.2,
        lanes=[Lane(4, 12.4), Lane(20.8, 29.2)],
        fixed_nodes=fixed_nodes,
        sections=[Section(
            patches=[
                Patch(-0.2, -1.075, 0, 1.075),
                Patch(-1.25, -0.25, -0.2, 0.25)
            ], layers=[
                Layer(-0.04, -1.035, -0.04, 0.21, num_fibers=16,
                      area_fiber=4.9e-4),
                Layer(-1.21, -0.21, -1.21, 0.21, num_fibers=5,
                      area_fiber=4.9e-4),
                Layer(-1.16, -0.21, -1.16, 0.21, num_fibers=6,
                      area_fiber=4.9e-4)
            ]
        )])
