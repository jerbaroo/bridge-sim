"""Make contour plots."""
import itertools
from typing import List

import matplotlib.cm as cm
import matplotlib.image as mpimg
import numpy as np

from classify.data.responses import responses_to_traffic_array
from classify.scenario.bridge import (
    PierDispBridge,
    equal_pier_disp,
    longitudinal_pier_disp,
)
from config import Config
from fem.params import SimParams
from fem.responses import Responses, load_fem_responses
from fem.run.opensees import OSRunner
from model.bridge import Point
from model.load import DisplacementCtrl, PointLoad
from model.response import ResponseType
from plot import plt
from plot.geom import top_view_bridge
from plot.responses import plot_contour_deck
from util import print_d, print_i, safe_str

# Print debug information for this file.
D: str = "make.plots.contour"
# D: bool = False


def plots_of_pier_displacement(c: Config):
    """Make contour plots of pier displacement."""
    y = 0
    response_types = [ResponseType.YTranslation]

    for response_type in response_types:
        for p, pier in list(enumerate(c.bridge.supports))[:1]:
            pier_disp = DisplacementCtrl(displacement=c.pd_unit_disp, pier=p)
            sim_params = SimParams(
                response_types=response_types, displacement_ctrl=pier_disp,
            )
            sim_responses = load_fem_responses(
                c=c,
                sim_params=sim_params,
                response_type=response_type,
                sim_runner=OSRunner(c),
                run=True,
            )
            top_view_bridge(c.bridge, abutments=True, piers=True)
            plot_contour_deck(
                c=c,
                responses=sim_responses,
                y=y,
                title=f"Pier displacement of {pier_disp.displacement} m",
                ploads=[
                    PointLoad(
                        x_frac=c.bridge.x_frac(pier.disp_node.x),
                        z_frac=c.bridge.z_frac(pier.disp_node.z),
                        kn=c.pd_unit_load_kn,
                    )
                ],
                center_norm=True,
            )
            plt.savefig(
                c.get_image_path(
                    "contour-pier-displacement",
                    safe_str(f"{response_type.name()}-pier-{p}"),
                )
            )
            plt.close()


def gradient_pier_displacement_plots(c: Config):
    """Contour plot of piers displaced in an increasing gradient."""
    for response_type in [ResponseType.YTranslation]:

        # Equal pier displacement scenario.
        for displacement in np.array([0.1, 0.01]) / 1000:
            gradient_pier_displacement_plot(
                c=c,
                pier_disp=equal_pier_disp(
                    bridge=c.bridge, displacement=displacement
                ),
                response_type=response_type,
                title=f"{response_type.name()} when each pier is displaced by {displacement} m",
            )

        # Gradient pier displacement scenario.
        for start, step in itertools.product(
            [0.01, 0.02, 0.05], [0.01, 0.02, 0.05]
        ):
            start, step = np.array([start, step]) / 1000
            gradient_pier_displacement_plot(
                c=c,
                pier_disp=longitudinal_pier_disp(
                    bridge=c.bridge, start=start, step=step
                ),
                response_type=response_type,
                title=f"{response_type.name()} when piers are incrementally displaced by {step} m starting at {start} m",
            )


def gradient_pier_displacement_plot(
    c: Config,
    pier_disp: PierDispBridge,
    response_type: ResponseType,
    title: str,
):
    """Contour plot of piers displaced in an increasing gradient."""

    # 10 x 10 grid of points on the bridge deck where to record responses.
    points = [
        Point(x=x, y=0, z=z)
        for x, z in itertools.product(
            np.linspace(c.bridge.x_min, c.bridge.x_max, 10),
            np.linspace(c.bridge.z_min, c.bridge.z_max, 10),
        )
    ]

    # Create empty traffic array and collect responses.
    response_array = responses_to_traffic_array(
        c=c,
        traffic_array=np.zeros(
            (1, len(c.bridge.wheel_tracks(c)) * c.il_num_loads)
        ),
        response_type=response_type,
        bridge_scenario=pier_disp,
        points=points,
        fem_runner=OSRunner(c),
    )

    top_view_bridge(c.bridge, abutments=True, piers=True)
    responses = Responses.from_responses(
        response_type=response_type,
        responses=[
            (response_array[0][p], point) for p, point in enumerate(points)
        ],
    )
    plot_contour_deck(c=c, responses=responses, center_norm=True)
    plt.title(title)
    plt.savefig(
        c.get_image_path(
            "pier-scenarios", f"pier-displacement-{safe_str(title)}"
        )
    )
    plt.close()


def comparison_plots_705(c: Config):
    """Make contour plots for all verification points on bridge 705."""
    positions = [
        (35, 25 - 16.6, None),
        (34.95459, 29.22606 - 16.6, "a"),
        (51.25051, 16.6 - 16.6, "b"),
        (92.40638, 12.405 - 16.6, "c"),
        (101.7649, 3.973938 - 16.6, "d"),
    ]
    response_types = [ResponseType.Strain]
    response_types = [ResponseType.Stress]
    response_types = [ResponseType.YTranslation]
    # For each response type and loading position first create contour plots for
    # OpenSees. Then finally create subplots comparing to Diana.
    for response_type in response_types:
        for load_x, load_z, label in positions:
            loads = [
                PointLoad(
                    x_frac=c.bridge.x_frac(load_x),
                    z_frac=c.bridge.z_frac(load_z),
                    kn=100,
                )
            ]
            fem_responses = load_fem_responses(
                c=c,
                response_type=response_type,
                sim_runner=OSRunner(c),
                sim_params=SimParams(
                    ploads=loads, response_types=response_types
                ),
            )
            title = (
                f"{response_type.name()} from a {loads[0].kn} kN point load"
                + f" at x = {load_x:.3f}m, z = {load_z:.3f}m"
            )
            save = lambda prefix: c.get_image_path(
                "contour",
                safe_str(
                    f"{prefix}{response_type.name()}-loadx={load_x:.3f}-loadz={load_z:.3f}"
                ),
            )
            # Plot once without colormaps centered to 0.
            top_view_bridge(c.bridge, piers=True, abutments=True)
            plot_contour_deck(
                c=c, responses=fem_responses, ploads=loads, title=title,
            )
            plt.savefig(save(""))
            plt.close()

            # Plot again with colormaps centered to 0.
            top_view_bridge(c.bridge, piers=True, abutments=True)
            plot_contour_deck(
                c=c,
                responses=fem_responses,
                ploads=loads,
                center_norm=True,
                title=title,
            )
            plt.savefig(save("center_norm-"))
            plt.close()

            # Finally create label/title the Diana plot.
            if label is not None:
                di_img = mpimg.imread(f"data/verification/diana-{label}.png")
                plt.imshow(di_img)
                plt.title(title)
                plt.xlabel("x position (mm)")
                plt.ylabel("z position (mm)")
                plt.savefig(save("diana-"))
                plt.close()


def plot_of_unit_loads(c: Config):
    """Make a contour plot of response at unit load position."""
    fem_runner = OSRunner(c)
    response_type = ResponseType.YTranslation
    X, Z, R = [], [], []
    for x in np.linspace(c.bridge.x_min, c.bridge.x_max, int(c.bridge.length)):
        X.append([])
        Z.append([])
        R.append([])
        for z in np.linspace(
            c.bridge.z_min, c.bridge.z_max, int(c.bridge.width)
        ):
            pload = PointLoad(
                x_frac=c.bridge.x_frac(x), z_frac=c.bridge.z_frac(z), kn=100
            )
            fem_params = SimParams(
                ploads=[pload], response_types=[response_type]
            )
            fem_responses = load_fem_responses(
                c=c,
                fem_params=fem_params,
                response_type=response_type,
                fem_runner=fem_runner,
            )
            X[-1].append(x)
            Z[-1].append(z)
            R[-1].append(fem_responses._at(x=x, y=0, z=z))

    cmap = cm.get_cmap("bwr")
    plt.contourf(X, Z, R, levels=50, cmap=cmap)
    plt.show()
