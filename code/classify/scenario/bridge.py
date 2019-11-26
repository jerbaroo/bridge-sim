"""Bridge scenarios."""
from model.scenario import BridgeScenario
from model.load import DisplacementCtrl
from util import round_m


class HealthyBridge(BridgeScenario):
    def __init__(self):
        super().__init__(name="normal")


class PierDispBridge(BridgeScenario):
    def __init__(self, pier_disps: [DisplacementCtrl]):
        name = "-".join(list(map(lambda pd: pd.id_str())))
        print(name)
        import sys; sys.exit()
        super().__init__(name=name)
        if len(pier_disps) > 0:
            raise ValueError("At least 1 PierDisp required")
        self.pier_disps = pier_disps
