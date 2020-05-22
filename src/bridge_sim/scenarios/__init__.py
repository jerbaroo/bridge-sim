"""Bridge scenarios, damage, temperature etc."""

from copy import copy, deepcopy
from typing import Callable, Tuple

from bridge_sim.model import Config, Bridge
from lib.fem.params import SimParams


class DamageScenario:
    def __init__(
        self,
        name: str,
        mod_bridge: Callable[[Bridge], Bridge] = lambda b: b,
        mod_sim_params: Callable[[SimParams], SimParams] = lambda s: s,
    ):
        """Base class for bridge scenarios.

        :param name: unique identifier for this bridge scenario.
        :param mod_bridge: function to modify a Bridge.
        :param mod_sim_params: function to modify simulation parameters.
        """
        self.name = name
        self.mod_bridge = mod_bridge
        self.mod_sim_params = mod_sim_params

    def use(
        self, c: Config, sim_params: SimParams = SimParams(),
    ) -> Tuple[Config, SimParams]:
        """Modify given Config and SimParams under this Scenario.

        The returned values are deep copies of the given objects.

        :param c: simulation configuration object to maybe modify.
        :param sim_params: simulation parameters to maybe modify.
        :return: a tuple of Config and SimParams.
        """
        config_copy = copy(c)
        config_copy.bridge = self.mod_bridge(deepcopy(config_copy.bridge))
        sim_params_copy = self.mod_sim_params(deepcopy(sim_params))
        return config_copy, sim_params_copy
