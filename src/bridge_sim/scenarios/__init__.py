"""Bridge scenarios, damage, temperature etc."""

from copy import copy, deepcopy
from typing import Callable, Tuple

from bridge_sim.model import Config, Bridge
from lib.fem.params import SimParams


class DamageScenario:
    """Abstract class for scenarios scenarios."""

    def __init__(
        self,
        name: str,
        mod_bridge: Callable[[Bridge], Bridge] = lambda b: b,
        mod_sim_params: Callable[[SimParams], SimParams] = lambda s: s,
    ):
        self.name = name
        self.mod_bridge = mod_bridge
        self.mod_sim_params = mod_sim_params

    def use(
        self, c: Config, sim_params: SimParams = SimParams(),
    ) -> Tuple[Config, SimParams]:
        """Copies of the given arguments modified for this scenarios scenario."""
        config_copy = copy(c)
        config_copy.bridge = self.mod_bridge(deepcopy(config_copy.bridge))
        sim_params_copy = self.mod_sim_params(deepcopy(sim_params))
        return config_copy, sim_params_copy
