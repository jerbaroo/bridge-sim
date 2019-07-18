"""Test that OpenSees builds model files correctly."""
import os
from timeit import default_timer as timer

from config import bridge_705_config
from fem.params import FEMParams
from fem.responses import fem_responses_path, load_fem_responses
from fem.run.opensees import os_runner
from model import *


def test_fem_responses():
    # Setup.
    reset_model_ids()
    c = bridge_705_config()
    fem_params = FEMParams([Load(0.1, 1000)])
    response_type = ResponseType.XTranslation
    fem_runner = os_runner(c)

    # Remove results on disk.
    path = fem_responses_path(
        c, fem_params, response_type, fem_runner.name)
    if os.path.exists(path):
        os.remove(path)

    # Run tests for each ResponseType.
    for response_type in ResponseType:
        fem_responses = load_fem_responses(
            c, fem_params, response_type, fem_runner)
        assert len(fem_responses.times) == 1
        assert fem_responses.times[0] == 0
