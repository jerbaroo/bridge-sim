"""Bridge scenarios."""
from model.bridge import Bridge
from model.load import DisplacementCtrl
from model.scenario import BridgeScenario
from util import round_m


class HealthyBridge(BridgeScenario):
    def __init__(self):
        super().__init__(name="normal")


class PierDispBridge(BridgeScenario):
    def __init__(self, pier_disps: [DisplacementCtrl], name_prefix: str = ""):
        if len(pier_disps) < 1:
            raise ValueError("At least 1 PierDisp required")
        name = name_prefix + "-".join(list(map(lambda pd: pd.id_str(), pier_disps)))
        super().__init__(name=name)
        self.pier_disps = pier_disps


def equal_pier_disp(bridge: Bridge, displacement: float):
    """All piers with equal given displacement."""
    return PierDispBridge(
        pier_disps=[
            DisplacementCtrl(displacement=displacement, pier=p)
            for p in range(len(bridge.supports))
        ],
        name_prefix="equal-piers",
    )


def longitudinal_pier_disp(bridge: Bridge, start: float, step: float):
    """Pier displacement that increases in longitudinal direction."""
    increase_every = len(set(pier.z for pier in bridge.supports))
    pier_disps = []
    displacement = start
    for p in range(len(bridge.supports)):
        if p != 0 and p % increase_every == 0:
            displacement += step
        pier_disps.append(DisplacementCtrl(displacement=displacement, pier=p))
    return PierDispBridge(pier_disps=pier_disps, name_prefix="longitudinal")
