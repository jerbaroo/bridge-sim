"""Test fem.run.opensees.parse."""
import itertools

from fem.params import ExptParams, FEMParams
from fem.run.opensees import OSRunner
from model.bridge.bridge_705 import bridge_705_3d, bridge_705_test_config
from model.load import PointLoad
from model.response import ResponseType


def test_parse_3d():
    """Test parsing of responses from a 3D OpenSees simulation."""
    c = bridge_705_test_config(bridge_705_3d)
    fem_runner = OSRunner(c)
    fem_params = FEMParams(
        ploads=[PointLoad(0.65, 0.35, 100)],
        response_types=[ResponseType.YTranslation])
    parsed = fem_runner.run(
        ExptParams([fem_params]), return_parsed=True, simple_mesh=True)
    # Index parsed responses by simulation, here is only one simulation.
    parsed_y_responses = parsed[0][ResponseType.YTranslation]
    # There should only be one time step.
    assert len(parsed_y_responses) == 1
    # Check that all deck nodes are recorded.
    assert len(parsed_y_responses[0]) == (
        c.bridge.base_mesh_deck_nodes_x * c.bridge.base_mesh_deck_nodes_z
        + c.bridge.base_mesh_pier_nodes_y * c.bridge.base_mesh_pier_nodes_z
        * len(c.bridge.supports) * 2)
