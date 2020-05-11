from typing import List

from classify.scenario.traffic import normal_traffic
from config import Config


def wheel_tracks(c: Config) -> List[float]:
    """Z positions of each wheel track on the bridge.

    This assumes that all vehicles drive along the center of a lane and have
    equal axis widths.

    """
    tracks = []

    # A moving vehicle for each bridge lane.
    mv_vehicles = [
        next(
            normal_traffic(c=c, lam=1, min_d=1).mv_vehicles(bridge=c.bridge, lane=lane)
        )(traffic=[], time=0, full_lanes=0)
        for lane in range(len(c.bridge.lanes))
    ]

    # From the moving vehicles we can calculate wheel tracks on the bridge.
    for mv_vehicle in mv_vehicles:
        for wheel_z_frac in mv_vehicle.wheel_tracks(bridge=c.bridge, meters=False):
            tracks.append(wheel_z_frac)

    return tracks
