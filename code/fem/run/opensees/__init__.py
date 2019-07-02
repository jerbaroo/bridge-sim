"""Run FEM simulations with OpenSees."""
import numpy as np

from config import Config
from fem.params import FEMParams
from fem.responses import FEMResponses
from fem.run import FEMRunner
from fem.run.opensees.build import build_model
from fem.run.opensees.run import run_model
from model import *


def _os_runner(c: Config, fem_params: FEMParams, runner_name: str):
    """Generate FEMResponses for given FEMParams (for each ResponseType)."""
    responses = [0 for _ in range(len(fem_params.simulations))]
    for i, loads in enumerate(fem_params.simulations):
        build_model(c, loads=loads)
        responses[i] = run_model(c)
    for response_type in Response:
        FEMResponses(
            fem_params,
            runner_name,
            response_type,
            map(lambda r: r[response_type], responses)
        ).save(c)


os_runner = FEMRunner(_os_runner, "OpenSees")
