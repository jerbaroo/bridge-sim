"""Verification plots."""
import numpy as np

from config import Config
from fem.params import SimParams
from fem.responses import load_fem_responses
from fem.run.opensees import OSRunner
from model.bridge import Point
from model.bridge.bridge_705 import bridge_705_3d, bridge_705_config
from model.load import PointLoad
from model.response import ResponseType
from plot import plt


def plot_convergence(c: Config):
    """Plot responses as shell density is increased."""
    response_type = ResponseType.YTranslation
    point = Point(x=35, y=0, z=9.4)
    bridge = bridge_705_3d()
    fem_params = SimParams(
        ploads=[PointLoad(
            x_frac=bridge.x_frac(point.x), z_frac=bridge.z_frac(point.z),
            kn=100)],
        response_types=[response_type])
    steps = 100
    xs = np.linspace(2, c.bridge.length, steps)
    zs = np.linspace(2, c.bridge.width, steps)
    responses = []
    for step in range(steps):
        x, z = int(xs[step]), int(zs[step])
        print(f"step = {step}, x = {x}, z = {z}")
        def bridge_overload(*args, **kwargs):
            return bridge_705_3d(
                name=f"Bridge 705-debug-{x}-{z}",
                base_mesh_deck_nodes_x=x,
                base_mesh_deck_nodes_z=z,
                base_mesh_pier_nodes_y=3,
                base_mesh_pier_nodes_z=3, *args, **kwargs)
        c = bridge_705_config(bridge_overload)
        fem_responses = load_fem_responses(
            c=c, fem_params=fem_params, response_type=response_type,
            fem_runner=OSRunner(c))
        responses.append(fem_responses._at(x=point.x, y=point.y, z=point.z))
    plt.plot(responses)
    plt.show()
