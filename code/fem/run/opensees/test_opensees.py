"""Full pipeline tests for OpenSees FEMRunner."""
from fem.params import ExptParams, SimParams
from fem.responses import load_fem_responses
from fem.run.opensees import OSRunner
from model.bridge import Fix, Layer, Patch
from model.bridge.bridge_705 import bridge_705_2d, bridge_705_3d, bridge_705_test_config
from model.load import PointLoad
from model.response import ResponseType
from util import clean_generated


def test_run_3d_model():
    """Test that OpenSees can run a 3D bridge model."""
    c = bridge_705_test_config(bridge_705_3d)
    c.os_node_step = c.bridge.length / 10
    c.os_node_step_z = c.bridge.width / 10
    clean_generated(c)
    expt_params = ExptParams([SimParams(
        ploads=[PointLoad(0.65, 0.35, 100)], response_types=[
            ResponseType.YTranslation, ResponseType.Strain])])
    OSRunner(c).run(expt_params)


def test_opensees_patch():
    """Test that all patch points are recorded."""
    # TODO: Fix 2D model.
    return
    num_sub_div_z = 20
    patch = Patch(
        y_min=-1, y_max=0, z_min=-1, z_max=1, num_sub_div_z=num_sub_div_z)

    def bridge_overload(*args, **kwargs):
        return bridge_705_2d(
            width=2,
            patches=[patch],
            layers=[Layer(
                y_min=-0.5, y_max=-0.5, z_min=-0.5, z_max=0.5, num_fibers=2)],
            *args, **kwargs)

    c = bridge_705_test_config(bridge_overload)
    clean_generated(c)
    fem_params = SimParams(
        ploads=[PointLoad(0.65, 0.35, 1234)], response_types=[
            ResponseType.YTranslation, ResponseType.Strain])
    fem_responses = load_fem_responses(
        c=c, fem_params=fem_params, response_type=ResponseType.Strain,
        fem_runner=OSRunner(c))
    # Ensure each patch point is accessible in results.
    x = c.os_node_step / 2  # Collected on the first element.
    for point in patch.points():
        _ = fem_responses.responses[0][x][point.y][point.z]
