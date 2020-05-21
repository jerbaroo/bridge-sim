"""Traffic scenarios."""
from timeit import default_timer as timer

import numpy as np

from bridge_sim.model.config import Config
from lib.model.scenario import TrafficScenario
from lib.vehicles.sample import sample_vehicle
from util import print_d, st

D: str = "classify.scenario.traffic"
D: bool = False  # Comment/uncomment to print debug statements for this file.


def arrival(beta: float, min_d: float):
    """Inter-arrival times of vehicles to the bridge."""
    result = np.random.exponential(beta)
    assert isinstance(result, float)
    if result < min_d:
        return arrival(beta=beta, min_d=min_d)
    return result


def normal_traffic(c: Config, lam: float, min_d: float):
    """Normal traffic scenario, arrives according to poisson process."""
    count = 0

    def mv_vehicle_f(time: float, full_lanes: int):
        start = timer()
        vehicle = sample_vehicle(c), arrival(beta=lam, min_d=min_d)
        nonlocal count
        count += 1
        print_d(D, f"{count}{st(count)} sampled vehicle took {timer() - start}")
        return vehicle

    return TrafficScenario(name=f"normal-lam-{lam}", mv_vehicle_f=mv_vehicle_f)


def heavy_traffic_1(c: Config, lam: float, min_d: float, prob_heavy: float):
    """Heavy traffic scenario.

    In this scenario a heavy vehicle instead of a normal vehicle is introduced
    on the bridge with given probability after traffic has warmed up.

    """
    assert 0 <= prob_heavy <= 1

    normal_traffic_scenario = normal_traffic(c=c, lam=lam, min_d=min_d)
    heavy_generated = False  # Have we created a heavy vehicle yet or not.
    the_heavy = sample_vehicle(c)  # Load intensity set later.
    max_kn = 0
    the_heavy.kn = 500

    def mv_vehicle_f(time: float, full_lanes: int):
        nonlocal heavy_generated
        nonlocal max_kn
        if not heavy_generated and full_lanes > 1:
            heavy_generated = True
            # the_heavy.kn = max_kn * 5
            return the_heavy, arrival(beta=lam, min_d=min_d)
        # Otherwise just the normal scenario.
        normal, dist = normal_traffic_scenario.mv_vehicle_f(
            time=time, full_lanes=full_lanes
        )
        max_kn = max(max_kn, normal.total_kn())
        return normal, dist

    return TrafficScenario(name="heavy-1", mv_vehicle_f=mv_vehicle_f)
