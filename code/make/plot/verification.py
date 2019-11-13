"""Verification plots."""
import os
from timeit import default_timer as timer

import numpy as np

from config import Config
from fem.params import SimParams
from fem.responses import load_fem_responses
from fem.run.opensees import OSRunner
from fem.run.opensees.build.d3 import nodes_by_id
from model.bridge import Point
from model.bridge.bridge_705 import bridge_705_3d, bridge_705_config
from model.load import PointLoad
from model.response import ResponseType
from plot import plt
from util import clean_generated


def plot_convergence(c: Config, run: bool):
    """Plot responses as shell density is increased.

    NOTE: This is a simplistic plot. After running this function with argument
    'run=True' on a few different machines, the results should be gathered as
    specified in the function 'plot_convergence_machines' and that function run
    to generate a better plot.

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
            *args,
            **kwargs,
        )

    c = bridge_705_config(bridge_overload)
    path = c.get_image_path("convergence", "node-density")

    if run:
        with open(path + ".txt", "w") as f:
            f.write("x, z, decknodes, time, responses...")
        steps = 10
        xs = np.linspace(2, 11, steps)
        zs = np.linspace(2, 11, steps)
        # steps = 100
        # xs = np.linspace(2, c.bridge.length * 4, steps)
        # zs = np.linspace(2, c.bridge.width * 4, steps)
        for step in range(steps):
            clean_generated(c)
            x, z = int(xs[step]), int(zs[step])
            with open(path + ".txt", "a") as f:
                f.write(f"\n{x}, {z}")
            c = bridge_705_config(bridge_overload)
            start = timer()
            sim_responses = load_fem_responses(
                c=c,
                sim_params=fem_params,
                response_type=response_type,
                sim_runner=OSRunner(c),
            )
            response = sim_responses._at(x=point.x, y=point.y, z=point.z)
            deck_nodes = len([n for n in nodes_by_id.values() if n.deck])
            with open(path + ".txt", "a") as f:
                f.write(f", {deck_nodes}, {timer() - start}, {response}")

    with open(path + ".txt") as f:
        results = list(map(
            lambda l: float(l.split()[-1]),
            filter(lambda l: len(l.split()) > 2, f.readlines()[1:])))
    plt.plot(results)
    plt.savefig(path)
    plt.close()
