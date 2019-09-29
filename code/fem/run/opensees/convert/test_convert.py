"""Test fem.run.opensees.convert."""
from fem.params import ExptParams, FEMParams
from fem.run.opensees import OSRunner
from fem.run.opensees.common import num_deck_nodes
from model import Response
from model.bridge.bridge_705 import bridge_705_3d, bridge_705_test_config
from model.load import Load
from model.response import ResponseType


def test_convert_3d():
    """Test converting of responses from a 3D OpenSees simulation."""
    c = bridge_705_test_config(bridge_705_3d)
    fem_runner = OSRunner(c)
    fem_params = FEMParams(
        loads=[Load(0.65, 100)], response_types=[ResponseType.YTranslation])
    converted = fem_runner.run(ExptParams([fem_params]), return_converted=True)
    # Index converted responses by simulation, here is only one simulation.
    converted_y_responses = converted[0][ResponseType.YTranslation]
    assert isinstance(converted_y_responses[0], Response)
    # Check that all deck nodes are recorded.
    num_deck_nodes_x, num_deck_nodes_z = num_deck_nodes(c)
    assert len(converted_y_responses) == num_deck_nodes_x * num_deck_nodes_z
