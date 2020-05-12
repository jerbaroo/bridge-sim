from typing import List, Optional

from bridge_sim.model import PierSettlement
from lib.config import Config as LibConfig
from lib.fem.params import SimParams as LibSimParams
from lib.fem.responses import load_fem_responses as lib_load_fem_responses
from lib.model.load import PointLoad as LibPointLoad
from lib.model.response import ResponseType as LibResponseType


def responses(
    config: LibConfig,
    response_type: LibResponseType,
    point_loads: List[LibPointLoad] = [],
    pier_settle: Optional[PierSettlement] = None,
):
    return lib_load_fem_responses(
        c=config,
        sim_params=LibSimParams(ploads=point_loads, displacement_ctrl=pier_settle),
        response_type=response_type,
    )
