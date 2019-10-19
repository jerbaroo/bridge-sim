"""Test fem.run.opensees.convert."""
from fem.params import ExptParams, FEMParams
from fem.run.opensees import OSRunner
from model import Response
from model.bridge.bridge_705 import bridge_705_3d, bridge_705_test_config
from model.load import PointLoad
from model.response import ResponseType


def test_convert_3d():
    """Test converting of responses from a 3D OpenSees simulation."""
    c = bridge_705_test_config(bridge_705_3d)
    fem_runner = OSRunner(c)
    fem_params = FEMParams(
        ploads=[PointLoad(0.65, 0.35, 100)],
        response_types=[ResponseType.YTranslation])
    converted = fem_runner.run(
        ExptParams([fem_params]), return_converted=True,
        include_support_3d_nodes=False)
    # Index converted responses by simulation, here is only one simulation.
    converted_y_responses = converted[0][ResponseType.YTranslation]
    assert isinstance(converted_y_responses[0], Response)
    # Check that all deck nodes are recorded.
    assert len(converted_y_responses) == (
        c.bridge.base_mesh_deck_nodes_x * c.bridge.base_mesh_deck_nodes_z)
