"""Test fem.run.opensees."""

from fem.params import ExptParams, FEMParams
from fem.responses import load_fem_responses
from fem.run.opensees import OSRunner
from model.bridge import Fix, Patch
from model.bridge.bridge_705 import Layer, Patch, bridge_705_config
from model.load import Load
from model.response import ResponseType
from util import clean_generated


def test_opensees_patch():
    num_sub_div_z = 20
    patch = Patch(
        y_min=-1, y_max=0, z_min=-1, z_max=1, num_sub_div_z=num_sub_div_z)
    c = bridge_705_config(
        width=2,
        patches=[patch],
        layers=[Layer(
            y_min=-0.5, y_max=-0.5, z_min=-0.5, z_max=0.5, num_fibers=2)],
        generated_dir="generated-data-test")
    clean_generated(c)
    fem_params = FEMParams(
        loads=[Load(0.65, 1234)],
        response_types=[
            ResponseType.YTranslation, ResponseType.Strain])
    fem_responses = load_fem_responses(
        c=c, fem_params=fem_params, response_type=ResponseType.Strain,
        fem_runner=OSRunner(c))
    # Ensure each patch point is accessible in results.
    x = c.os_node_step / 2  # Collected on the first element.
    for point in patch.points():
        _ = fem_responses.responses[0][x][point.y][point.z]
