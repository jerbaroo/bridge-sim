from typing import List, Optional

from bridge_sim.model import (
    PierSettlement,
    PointLoad,
    ResponseType,
    Config as LibConfig,
)
from lib.fem.params import SimParams as LibSimParams
from lib.fem.responses import load_fem_responses as lib_load_fem_responses


def responses(
    config: LibConfig,
    response_type: ResponseType,
    point_loads: List[PointLoad] = [],
    pier_settlement: Optional[PierSettlement] = None,
):
    """Responses from a single linear simulation.

    The simulation is only run if necessary (results not on disk).

    Args:
        config: Global configuration object.
        response_type: Sensor response type to return.
        point_loads: Point loads to apply in simulation.
        pier_settlement: A pier settlement to apply.
    """
    return lib_load_fem_responses(
        c=config,
        sim_params=LibSimParams(ploads=point_loads, displacement_ctrl=pier_settlement),
        response_type=response_type,
    )
