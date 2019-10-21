"""Different scenarios for data generation."""
from config import Config
from model.load import DisplacementCtrl
from model.scenario import BridgeScenario, TrafficScenario
from vehicles.sample import sample_vehicle
from util import round_m


# TODO: Move to model.scenarios.


def normal_traffic(c: Config):
    return TrafficScenario(name="normal", mv_vehicle_f=lambda: (sample_vehicle(c), 5))


# heavy_traffic = TrafficScenario(name="heavy", vehicle=None)


class BridgeScenarioNormal(BridgeScenario):
    def __init__(self):
        super().__init__(name="normal")


class BridgeScenarioDisplacementCtrl(BridgeScenario):
    def __init__(self, displacement_ctrl: DisplacementCtrl):
        super().__init__(
            name=f"displacement-{round_m(displacement_ctrl.displacement)}m"
                 + f"-pier-{displacement_ctrl.pier}")
        self.displacement_ctrl = displacement_ctrl
