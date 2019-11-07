"""Bridge scenarios."""
from model.scenario import BridgeScenario
from model.load import DisplacementCtrl
from util import round_m


class HealthyBridge(BridgeScenario):
    def __init__(self):
        super().__init__(name="normal")


class PierDispBridge(BridgeScenario):
    def __init__(self, displacement_ctrl: DisplacementCtrl):
        super().__init__(
            name=f"displacement-{round_m(displacement_ctrl.displacement)}m"
                 + f"-pier-{displacement_ctrl.pier}")
        self.displacement_ctrl = displacement_ctrl
