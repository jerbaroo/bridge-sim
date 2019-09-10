"""Different scenarios for data generation."""
from config import Config
from model.load import DisplacementCtrl
from model.scenario import BridgeScenario, TrafficScenario
from vehicles.sample import sample_vehicle
from util import round_m


def normal_traffic(c: Config):
    return TrafficScenario(
        c=c,
        name="normal",
        vehicle=lambda c: (sample_vehicle(c), 10))


def heavy_traffic(c: Config):
    return TrafficScenario(
        c=c,
        name="heavy",
        vehicle=None)


class BridgeScenarioNormal(BridgeScenario):
    def __init__(self):
        super().__init__(name="normal")


class BridgeScenarioDisplacementCtrl(BridgeScenario):
    def __init__(self, displacement_ctrl: DisplacementCtrl):
        super().__init__(
            name=f"displacement-{round_m(displacement_ctrl.displacement)}m"
                 + f"-pier-{displacement_ctrl.pier}")
        self.displacement_ctrl = displacement_ctrl
