"""Different scenarios for data generation."""
# TODO: Move to model.scenarios.
import numpy as np
from copy import deepcopy

from config import Config
from model.load import DisplacementCtrl
from model.scenario import BridgeScenario, TrafficScenario
from vehicles.sample import sample_vehicle
from util import round_m, print_d

# Comment/uncomment to print debug statements for this file.
D: str = "classify.data.scenarios"
D: bool = False


def arrival(beta: float):
    """Inter-arrival times of vehicles to the bridge."""
    result = np.random.exponential(beta)
    print(f"Inter-vehicle distance = {result}")
    assert isinstance(result, float)
    return result


def normal_traffic(c: Config, lam: float):
    """Normal traffic scenario, arrives according to poisson process."""

    def mv_vehicle_f(traffic: "Traffic", time: float, full_lanes: int):
        # print(f"normal_traffic received traffic {type(traffic)} {time}")
        return sample_vehicle(c), arrival(lam)

    return TrafficScenario(name=f"normal-lam-{lam}", mv_vehicle_f=mv_vehicle_f)


def heavy_traffic_1(c: Config, lam: float, prob_heavy: float):
    """Heavy traffic scenario.

    In this scenario a heavy vehicle instead of a normal vehicle is introduced
    on the bridge with given probability after traffic has warmed up.

    """
    assert 0 <= prob_heavy <= 1

    normal_traffic_scenario = normal_traffic(c=c, lam=lam)
    heavy_generated = False  # Have we created a heavy vehicle yet or not.
    the_heavy = sample_vehicle(c)
    max_kn = 0

    def mv_vehicle_f(traffic: "Traffic", time: float, full_lanes: int):
        nonlocal heavy_generated; nonlocal max_kn
        if not heavy_generated and full_lanes >= 1:
            heavy_generated = True
            the_heavy.kn = max_kn * 10
            return the_heavy, arrival(lam)
        # Otherwise just the normal scenario.
        normal, dist = normal_traffic_scenario.mv_vehicle_f(
            traffic=traffic, time=time, full_lanes=full_lanes)
        max_kn = max(max_kn, normal.total_kn())
        return normal, dist

    return TrafficScenario(name="heavy-1", mv_vehicle_f=mv_vehicle_f)


class BridgeScenarioNormal(BridgeScenario):
    def __init__(self):
        super().__init__(name="normal")


class BridgeScenarioDisplacementCtrl(BridgeScenario):
    def __init__(self, displacement_ctrl: DisplacementCtrl):
        super().__init__(
            name=f"displacement-{round_m(displacement_ctrl.displacement)}m"
                 + f"-pier-{displacement_ctrl.pier}")
        self.displacement_ctrl = displacement_ctrl
