"""Make contour plots."""
from typing import List

import matplotlib.cm as cm
import numpy as np

from config import Config
from fem.params import SimParams
from fem.responses import load_fem_responses
from fem.run.opensees import OSRunner
from model.load import DisplacementCtrl, PointLoad
from model.response import ResponseType
from plot import plt
from plot.geom import top_view_bridge
from plot.responses import plot_contour_deck
from util import print_d, print_i, safe_str

# Print debug information for this file.
D: str = "make.plots.contour"
# D: bool = False


def plots_of_pier_displacement(
        c: Config, y: float, response_types: List[ResponseType]):
    """Make contour plots of pier displacement."""
    fem_runner = OSRunner(c)
    for response_type in response_types:
        for p, pier in enumerate(c.bridge.supports):
            fem_params = SimParams(
                response_types=response_types,
                displacement_ctrl=(
                    DisplacementCtrl(displacement=c.pd_unit_disp, pier=p)))
            fem_responses = load_fem_responses(
                c=c, fem_params=fem_params, response_type=response_type,
                fem_runner=fem_runner)
            top_view_bridge(c.bridge, lanes=False, outline=False)
            plot_contour_deck(
                c=c, responses=fem_responses, y=y,
                ploads=[PointLoad(
                    x_frac=c.bridge.x_frac(pier.disp_node.x),
                    z_frac=c.bridge.z_frac(pier.disp_node.z),
                    kn=c.pd_unit_load_kn)],
                save=(c.get_image_path("contour-pier-displacement", safe_str(
                    f"{response_type.name()}-pier-{p}"))))


def plots_for_verification(
        c: Config, y: float, response_types: List[ResponseType]):
    """Make contour plots for all verification points."""
    fem_runner = OSRunner(c)
    for response_type in response_types:
        for load_x, load_z in [
                (34.95459, 29.22606 - 16.6),  # A.
                (51.25051, 16.6     - 16.6),  # B.
                (92.40638, 12.405   - 16.6),  # C.
                (101.7649, 3.973938 - 16.6)]:  # D.
            print_i(f"Contour plot at x, z, = {load_x}, {load_z}")
            pload = PointLoad(
                x_frac=c.bridge.x_frac(load_x), z_frac=c.bridge.z_frac(load_z),
                kn=100)
            print_d(D, f"response_types = {response_types}")
            fem_params = SimParams(
                ploads=[pload], response_types=response_types)
            print_d(D, f"loading response type = {response_type}")
            fem_responses = load_fem_responses(
                c=c, sim_params=fem_params, response_type=response_type,
                sim_runner=fem_runner)
            plot_contour_deck(
                c=c, responses=fem_responses, y=y, ploads=[pload],
                save=(c.get_image_path("contour", safe_str(
                    f"{response_type.name()}-loadx={load_x}-loadz={load_z}"))))


def plot_of_unit_loads(c: Config):
    """Make a contour plot of response at unit load position."""
    fem_runner = OSRunner(c)
    response_type = ResponseType.YTranslation
    X, Z, R = [], [], []
    for x in np.linspace(c.bridge.x_min, c.bridge.x_max, int(c.bridge.length)):
        X.append([])
        Z.append([])
        R.append([])
        for z in np.linspace(c.bridge.z_min, c.bridge.z_max, int(c.bridge.width)):
            pload = PointLoad(
                x_frac=c.bridge.x_frac(x), z_frac=c.bridge.z_frac(z), kn=100)
            fem_params = SimParams(
                ploads=[pload], response_types=[response_type])
            fem_responses = load_fem_responses(
                c=c, fem_params=fem_params, response_type=response_type,
                fem_runner=fem_runner)
            X[-1].append(x)
            Z[-1].append(z)
            R[-1].append(fem_responses._at(x=x, y=0, z=z))

    cmap = cm.get_cmap("bwr")
    plt.contourf(X, Z, R, levels=50, cmap=cmap)
    plt.show()
