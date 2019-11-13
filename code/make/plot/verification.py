"""Verification plots."""
import os
from timeit import default_timer as timer

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
from util import clean_generated


def plot_convergence(c: Config, run: bool):
    """Plot responses as shell density is increased.

    Args:
        c: Config, global configuration object.
        run: bool, whether to re-run data collection simulations.

    """
    response_type = ResponseType.YTranslation
    point = Point(x=35, y=0, z=9.4)
    bridge = bridge_705_3d()
    fem_params = SimParams(
        ploads=[
            PointLoad(
                x_frac=bridge.x_frac(point.x),
                z_frac=bridge.z_frac(point.z),
                kn=100,
            )
        ],
        response_types=[response_type],
    )
    x, z = 2, 2

    def bridge_overload(*args, **kwargs):
        return bridge_705_3d(
            name=f"Bridge 705 convergence-plot",
            base_mesh_deck_nodes_x=x,
            base_mesh_deck_nodes_z=z,
            base_mesh_pier_nodes_y=5,
            base_mesh_pier_nodes_z=5,
            *args,
            **kwargs,
        )

    c = bridge_705_config(bridge_overload)
    path = c.get_image_path("convergence", "node-density")

    if run:
        with open(path + ".txt", "w") as f:
            pass  # Empty the file.
        steps = 100
        xs = np.linspace(2, c.bridge.length * 4, steps)
        zs = np.linspace(2, c.bridge.width * 4, steps)
        for step in range(steps):
            clean_generated(c)
            x, z = int(xs[step]), int(zs[step])
            with open(path + ".txt", "a") as f:
                f.write(f"\nx = {x}, z = {z}")
            c = bridge_705_config(bridge_overload)
            start = timer()
            sim_responses = load_fem_responses(
                c=c,
                sim_params=fem_params,
                response_type=response_type,
                sim_runner=OSRunner(c),
            )
            response = sim_responses._at(x=point.x, y=point.y, z=point.z)
            with open(path + ".txt", "a") as f:
                f.write(f", time = {timer() - start:.4f}, response = {response}")

    with open(path + ".txt") as f:
        results = list(map(
            lambda l: float(l.split()[-1]),
            filter(lambda l: len(l.split()) > 6, f.readlines())))
    plt.plot(results)
    plt.savefig(path)
    plt.close()
