"""Different scenarios for data generation."""
import numpy as np

from config import Config
from model.load import DisplacementCtrl
from model.scenario import BridgeScenario, TrafficScenario
from vehicles.sample import sample_vehicle
from util import round_m

# TODO: Move to model.scenarios.


def arrival(beta: float):
    result = np.random.exponential(beta)
    print(f"Inter-vehicle distance = {result}")
    assert isinstance(result, float)
    return result


def normal_traffic(c: Config, lam: float):
    """Normal traffic scenario, arrives according to poisson process."""
    return TrafficScenario(
        name=f"normal-lam-{lam}",
        mv_vehicle_f=lambda: (sample_vehicle(c), arrival(lam)))


def heavy_traffic_1(c: Config):
    """Heavy traffic scenario where the total load on the bridge is less than"""
    return TrafficScenario(
        name="heavy-1", mv_vehicle_f=lambda: ())


class BridgeScenarioNormal(BridgeScenario):
    def __init__(self):
        super().__init__(name="normal")


class BridgeScenarioDisplacementCtrl(BridgeScenario):
    def __init__(self, displacement_ctrl: DisplacementCtrl):
        super().__init__(
            name=f"displacement-{round_m(displacement_ctrl.displacement)}m"
                 + f"-pier-{displacement_ctrl.pier}")
        self.displacement_ctrl = displacement_ctrl
