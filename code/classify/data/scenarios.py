"""Different scenarios for data generation."""
from model.load import DisplacementCtrl
from model.scenario import BridgeScenario, TrafficScenario
from vehicles.sample import sample_vehicle

normal_traffic = TrafficScenario(name="normal", vehicle=sample_vehicle)
heavy_traffic = TrafficScenario(name="heavy", vehicle=None)


class BridgeScenarioNormal(BridgeScenario):
    def __init__(self):
        super().__init__(name="normal")


class BridgeScenarioDisplacementCtrl(BridgeScenario):
    def __init__(self, displacement_ctrl: DisplacementCtrl):
        super().__init__(
            name=f"displacement-{displacement_ctrl.displacement:.6f}m"
                 + f"-pier-{displacement_ctrl.pier}")
        self.displacement_ctrl = displacement_ctrl
