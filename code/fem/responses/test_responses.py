"""Test that OpenSees builds model files correctly."""
import os
from timeit import default_timer as timer

import numpy as np

from fem.params import SimParams
from fem.responses import fem_responses_path, load_fem_responses
from fem.run.opensees import OSRunner
from model.bridge import Layer
from model.bridge.bridge_705 import bridge_705_2d, bridge_705_test_config
from model.load import PointLoad
from model.response import ResponseType


def test_fem_responses():
    # Setup.
    return

    layer = Layer(y_min=-8, y_max=-8, z_min=-4.5, z_max=4.5, num_fibers=10)

    def bridge_overload(*args, **kwargs):
        return bridge_705_2d(layers=[layer], *args, **kwargs)

    c = bridge_705_test_config(bridge_705_2d)
    fem_runner = OSRunner(c)
    response_types = fem_runner.supported_response_types(c.bridge)
    fem_params = SimParams(
        ploads=[PointLoad(x_frac=0.1, z_frac=0.3, kn=1000)],
        response_types=response_types)

    # for response_type in list(ResponseType):
    for response_type in response_types:
        # Remove results on disk.
        path = fem_responses_path(
            c=c, fem_params=fem_params, response_type=response_type,
            runner_name=fem_runner.name)
        if os.path.exists(path):
            os.remove(path)
        print(response_type)
        print(path)

        # Load simulation responses for each ResponseType.
        print(f"Running load_fem_responses")
        fem_responses = load_fem_responses(
            c=c, fem_params=fem_params, response_type=response_type,
            fem_runner=fem_runner)
        # Check length of simulation results.
        assert len(fem_responses.times) == 1
        assert fem_responses.times[0] == 0
        assert os.path.exists(path)

    # For the x and y translation responses there should be one response for
    # each element, with only one response for each y and z axis.
    def assert_translation_responses_shape(response_type: ResponseType):
        fem_responses = load_fem_responses(
            c=c, fem_params=fem_params, response_type=response_type,
            fem_runner=fem_runner)
        assert np.isclose(
            len(fem_responses.xs), c.bridge.length / c.os_node_step + 1)
        assert len(fem_responses.ys[fem_responses.xs[0]]) == 1
        assert len(fem_responses.zs[fem_responses.xs[0]]) == 1
        assert len(fem_responses.zs[fem_responses.xs[0]][
            fem_responses.ys[fem_responses.xs[0]][0]]) == 1

    # assert_translation_responses_shape(ResponseType.XTranslation)
    # assert_translation_responses_shape(ResponseType.YTranslation)

    # For the stress and strain responses there should be one response for each
    # node, with one response for each y and z point of the layers and patches.
    def assert_stress_strain_responses_shape(response_type: ResponseType):
        fem_responses = load_fem_responses(
            c=c, fem_params=fem_params, response_type=response_type,
            fem_runner=fem_runner)
        assert np.isclose(
            len(fem_responses.xs), c.bridge.length / c.os_node_step)
        assert len(fem_responses.ys[fem_responses.xs[0]]) == (
            len(c.bridge.sections[0].patches) +
            len(c.bridge.sections[0].layers))
        assert len(fem_responses.zs[fem_responses.xs[0]]) == (
            len(c.bridge.sections[0].patches) +
            len(c.bridge.sections[0].layers))
        assert len(fem_responses.zs[fem_responses.xs[0]][
            fem_responses.ys[fem_responses.xs[0]][0]]) == len(layer.points())

    # assert_stress_strain_responses_shape(ResponseType.Strain)
    # assert_stress_strain_responses_shape(ResponseType.Stress)


def test_fem_responses_at():
    return
    # Setup.
    c = bridge_705_test_config(bridge_705_2d)
    fem_runner = OSRunner(c)
    response_types = fem_runner.supported_response_types(c.bridge)
    fem_params = SimParams(
        ploads=[PointLoad(x_frac=0.1, z_frac=0.3, kn=1000)],
        response_types=response_types)
    response_type = ResponseType.XTranslation

    # Load simulation responses.
    fem_responses = load_fem_responses(
        c=c, fem_params=fem_params, response_type=response_type,
        fem_runner=fem_runner)

    # Retrieve a response.
    x, y, z = fem_responses.xs[len(fem_responses.xs) // 2], 0, 0
    response_true = fem_responses.responses[0][x][y][z].value
    print(x)
    print(response_true)

    x_frac, y_frac, z_frac = c.bridge.x_frac(x), 0, 0
    print(x_frac, y_frac, z_frac)
    response_at = fem_responses.at(x_frac=x_frac, y_frac=y_frac, z_frac=z_frac)
    print(response_at)
