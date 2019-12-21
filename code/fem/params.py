"""Parameters for FEM simulations."""
from typing import List, Optional

from model.load import DisplacementCtrl, PointLoad
from model.response import ResponseType
from util import safe_str


class SimParams:
    """Parameters for one FEM simulation.

    Point loads XOR displacement control, and response types to record.

    Args:
        response_types: [ResponseType], response types to record.
        ploads: List[PointLoad], point loads to apply in the simulation.
        displacement_ctrl: DisplacementCtrl, apply a load until the given
            displacement in meters is reached.

    """

    def __init__(
        self,
        response_types: List[ResponseType],
        ploads: List[PointLoad] = [],
        displacement_ctrl: Optional[DisplacementCtrl] = None,
        axial_delta_temp: Optional[float] = None,
    ):
        self.response_types = response_types
        self.ploads = ploads
        self.displacement_ctrl = displacement_ctrl
        self.axial_delta_temp = axial_delta_temp
        self._assert()

    def _assert(self):
        """Maximum 1 load type should be applied (due to linear assumption)."""
        load_types = []
        if self.displacement_ctrl is not None:
            load_types.append(1)
        if self.axial_delta_temp is not None:
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
            load_str = f"temp-{self.axial_delta_temp}"
        elif len(self.ploads) > 0:
            load_str = ",".join(pl.id_str() for pl in self.ploads)
            load_str = f"[{load_str}]"
        else:
            return ""
        return safe_str(f"{responses_str}-{load_str}")


class ExptParams:
    """Parameters for multiple simulations.

    NOTE: Make into a NewType.

    """

    def __init__(self, sim_params: List[SimParams]):
        self.sim_params = sim_params
