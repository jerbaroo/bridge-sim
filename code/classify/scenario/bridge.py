"""Bridge scenarios."""
from copy import deepcopy
from typing import Callable

from config import Config
from model.bridge import Bridge
from model.load import DisplacementCtrl
from model.scenario import BridgeScenario
from util import round_m


class HealthyBridge(BridgeScenario):
    def __init__(self):
        super().__init__(name="normal")


class CrackedBridge(BridgeScenario):
    def __init__(self, name: str, crack: Callable[[Bridge], Bridge]):
        super().__init__(name=name)
        self.crack_f = crack

    def crack(self, bridge: Bridge) -> Bridge:
        cracked_bridge = self.crack_f(deepcopy(bridge))
        cracked_bridge.type = self.name
        return cracked_bridge

    def crack_config(self, config: Config) -> Config:
        config_copy = deepcopy(config)
        config_copy.bridge = self.crack(config_copy.bridge)
        return config_copy


def center_lane_crack(percent: float=10, lane: int=0) -> CrackedBridge:
    """A bridge with the center of a lane cracked."""

    def crack(bridge: Bridge) -> Bridge:
        # Get the position of the crack.
        x_start, z_start = bridge.x(0.45), bridge.lanes[lane].z_min
        length, width = bridge.x(percent / 100), bridge.lanes[lane].width
        print(f"x start = {x_start}, z_start = {z_start}")
        print(f"length = {length}, width = {width}")
        return bridge

    return CrackedBridge(
        name=f"crack-lane-{lane}-center-{percent}", crack=crack)


class PierDispBridge(BridgeScenario):
    def __init__(self, pier_disps: [DisplacementCtrl], name_prefix: str = ""):
        if len(pier_disps) < 1:
            raise ValueError("At least 1 PierDisp required")
        name = name_prefix + "-".join(list(map(lambda pd: pd.id_str(), pier_disps)))
        super().__init__(name=name)
        self.pier_disps = pier_disps


def equal_pier_disp(bridge: Bridge, displacement: float) -> PierDispBridge:
    """All piers with equal given displacement."""
    return PierDispBridge(
        pier_disps=[
            DisplacementCtrl(displacement=displacement, pier=p)
            for p in range(len(bridge.supports))
        ],
        name_prefix="equal-piers",
    )


def longitudinal_pier_disp(bridge: Bridge, start: float, step: float) -> PierDispBridge:
    """Pier displacement that increases in longitudinal direction."""
    increase_every = len(set(pier.z for pier in bridge.supports))
    pier_disps = []
    displacement = start
    for p in range(len(bridge.supports)):
        if p != 0 and p % increase_every == 0:
            displacement += step
        pier_disps.append(DisplacementCtrl(displacement=displacement, pier=p))
    return PierDispBridge(pier_disps=pier_disps, name_prefix="longitudinal")
