"""Test fem.run.opensees.parse."""
from fem.params import ExptParams, FEMParams
from fem.run.opensees import OSRunner
from fem.run.opensees.common import num_deck_nodes
from model.bridge.bridge_705 import bridge_705_3d, bridge_705_test_config
from model.load import Load
from model.response import ResponseType


def test_parse_3d():
    """Test parsing of responses from a 3D OpenSees simulation."""
    c = bridge_705_test_config(bridge_705_3d)
    fem_runner = OSRunner(c)
    fem_params = FEMParams(
        loads=[Load(0.65, 100)], response_types=[ResponseType.YTranslation])
    parsed = fem_runner.run(
        ExptParams([fem_params]), return_parsed=True, support_3d_nodes=False)
    # Index parsed responses by simulation, here is only one simulation.
    parsed_y_responses = parsed[0][ResponseType.YTranslation]
    # There should only be one time step.
    assert len(parsed_y_responses) == 1
    # Check that all deck nodes are recorded.
    num_deck_nodes_x, num_deck_nodes_z = num_deck_nodes(c)
    assert len(parsed_y_responses[0]) == num_deck_nodes_x * num_deck_nodes_z
