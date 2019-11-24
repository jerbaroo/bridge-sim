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
    ):
        if displacement_ctrl is not None:
            assert len(ploads) == 0
        self.response_types = response_types
        self.ploads = ploads
        self.displacement_ctrl = displacement_ctrl

    def id_str(self):
        """String representing the simulation parameters."""

        responses_str = "".join(r.name() for r in self.response_types)

        if self.displacement_ctrl is not None:
            load_str = self.displacement_ctrl.id_str()
        else:
            load_str = ",".join(pl.id_str() for pl in self.ploads)
            load_str = f"[{load_str}]"

        return safe_str(f"{responses_str}-{load_str}")


class ExptParams:
    """Parameters for multiple simulations.

    NOTE: Make into a NewType.

    """

    def __init__(self, sim_params: List[SimParams]):
        self.sim_params = sim_params
