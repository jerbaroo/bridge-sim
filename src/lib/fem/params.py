"""Parameters for FEM simulations."""
from typing import List, Optional

from bridge_sim.model import ResponseType, PierSettlement, PointLoad, Bridge
from lib.fem.model import BuildContext
from util import safe_str


class SimParams:
    """Parameters for one FEM simulation.

    Point loads XOR displacement control, and response types to record.

    Args:
        response_types: [ResponseType], response types to record.
        ploads: List[PointLoad], point loads to apply in the simulation.
        displacement_ctrl: PierSettlement, apply a load until the given
            displacement in meters is reached.
        axial_delta_temp: Optional[float], axial thermal loading in celcius.
        moment_delta_temp: Optional[float], moment thermal loading in celcius.
        refinement_radii: List[float], a list of mesh refinement radii as
            defined in 'BuildContext'.

    """

    def __init__(
        self,
        response_types: List[ResponseType] = ResponseType.all(),
        ploads: List[PointLoad] = [],
        displacement_ctrl: Optional[PierSettlement] = None,
        axial_delta_temp: Optional[float] = None,
        moment_delta_temp: Optional[float] = None,
        refinement_radii: List[float] = [],
        clean_build: bool = False,
    ):
        self.response_types = response_types
        self.ploads = ploads
        self.displacement_ctrl = displacement_ctrl
        self.axial_delta_temp = axial_delta_temp
        self.moment_delta_temp = moment_delta_temp
        self.refinement_radii = refinement_radii
        self.clean_build = clean_build
        self._assert()

    def build_ctx(self, bridge: Bridge) -> BuildContext:
        return BuildContext(
            add_loads=[pload.point() for pload in self.ploads],
            refinement_radii=self.refinement_radii,
        )

    def _assert(self):
        """Maximum 1 load type should be applied (due to linear assumption)."""
        load_types = []
        if self.displacement_ctrl is not None:
            load_types.append(1)
        if self.axial_delta_temp is not None:
            load_types.append(1)
        if self.moment_delta_temp is not None:
            load_types.append(1)
        if len(self.ploads) > 0:
            load_types.append(1)
        assert len(load_types) <= 1

    def id_str(self):
        """String representing the simulation parameters."""
        responses_str = "".join(r.name() for r in self.response_types)
        if self.displacement_ctrl is not None:
            load_str = self.displacement_ctrl.id_str()
        elif self.axial_delta_temp is not None:
            load_str = f"temp-axial-{self.axial_delta_temp}"
        elif self.moment_delta_temp is not None:
            load_str = f"temp-moment-{self.moment_delta_temp}"
        elif len(self.ploads) > 0:
            load_str = ",".join(pl.id_str() for pl in self.ploads)
            load_str = f"[{load_str}]"
        else:
            load_str = "no-loading"
        return safe_str(f"{responses_str}-{load_str}")


class ExptParams:
    """Parameters for multiple simulations.

    NOTE: Make into a NewType.

    """

    def __init__(self, sim_params: List[SimParams]):
        self.sim_params = sim_params
