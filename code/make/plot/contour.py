"""Make contour plots."""
import itertools
from itertools import chain
from typing import List, Tuple

import matplotlib.colors as colors
import matplotlib.image as mpimg
import numpy as np
from matplotlib.cm import get_cmap

from classify.data.responses import responses_to_traffic_array
from classify.scenario.bridge import (
    CrackedBridge,
    PierDispBridge,
    equal_pier_disp,
    longitudinal_pier_disp,
)
from classify.scenarios import cracked_scenario, all_scenarios
from classify.vehicle import wagen1
from config import Config
from fem.params import SimParams
from fem.responses import Responses, load_fem_responses
from fem.run.opensees import OSRunner
from make.plot.distribution import load_normal_traffic_array
from model.bridge import Point
from model.load import DisplacementCtrl, PointLoad
from model.response import ResponseType
from plot import parula_cmap, plt
from plot.contour import contour_responses_3d
from plot.geometry import top_view_bridge
from plot.responses import plot_contour_deck, resize_units
from util import print_d, print_i, safe_str

# Print debug information for this file.
D: str = "make.plots.contour"
# D: bool = False


def unit_axial_thermal_deck_load(c: Config):
    """Response to unit axial thermal deck loading."""
    response_types = [ResponseType.XTranslation, ResponseType.YTranslation, ResponseType.ZTranslation]
    for response_type in response_types:
        sim_responses = load_fem_responses(
            c=c,
            sim_runner=OSRunner(c),
            response_type=response_type,
            sim_params=SimParams(
                response_types=response_types,
                axial_delta_temp=c.unit_axial_delta_temp_c
            )
        )
        top_view_bridge(c.bridge, abutments=True, piers=True)
        plot_contour_deck(
            c=c,
            responses=sim_responses,
            levels=100,
        )
        plt.title(f"{response_type.name()} to {c.unit_axial_delta_temp_c}C axial thermal loading of the deck")
        plt.savefig(
            c.get_image_path("contour", f"thermal-deck-unit-axial_load-{response_type.name()}.pdf")
        )
        plt.close()


def unit_moment_thermal_deck_load(c: Config):
    """Response to unit moment thermal deck loading."""
    response_types = [ResponseType.XTranslation, ResponseType.YTranslation, ResponseType.ZTranslation]
    for response_type in response_types:
        sim_responses = load_fem_responses(
            c=c,
            sim_runner=OSRunner(c),
            response_type=response_type,
            sim_params=SimParams(
                response_types=response_types,
                moment_delta_temp=c.unit_moment_delta_temp_c
            )
        )
        top_view_bridge(c.bridge, abutments=True, piers=True)
        plot_contour_deck(
            c=c,
            responses=sim_responses,
            levels=100,
        )
        plt.title(f"{response_type.name()} to {c.unit_moment_delta_temp_c}C moment thermal loading of the deck")
        plt.savefig(
            c.get_image_path("contour", f"thermal-deck-unit-moment-load-{response_type.name()}.pdf")
        )
        plt.close()


def cover_photo(c: Config, x: float, deformation_amp: float):
    """

    TODO: SimParams takes any loads iterable, to be flattened.
    TODO: Wrap SimRunner into Config.
    TODO: Ignore response type in SimParams (fill in by load_sim_responses).

    """
    response_type=ResponseType.YTranslation
    sim_responses = load_fem_responses(
        c=c,
        sim_runner=OSRunner(c),
        response_type=response_type,
        sim_params=SimParams(
            response_types=[response_type],
            ploads=list(chain.from_iterable(
                wagen1.to_point_loads(
                    bridge=c.bridge,
                    time=wagen1.time_at(x=x, bridge=c.bridge),
                )
            ))
        )
    )
    shells = contour_responses_3d(c=c, sim_responses=sim_responses)
    for cmap in [parula_cmap, get_cmap("jet"), get_cmap("coolwarm"), get_cmap("viridis")]:

            contour_responses_3d(
                c=c,
                sim_responses=sim_responses,
                deformation_amp=deformation_amp,
                shells=shells,
                cmap=cmap,
            )

            plt.axis("off")
            plt.grid(False)
            plt.savefig(c.get_image_path(
                "cover-photo",
                f"cover-photo-deform-{deformation_amp}"
                f"-cmap-{cmap.name}.pdf"))
            plt.close()


def mean_traffic_response_plots(c: Config):
    """Mean response to normal traffic per damage scenario."""
    response_type = ResponseType.YTranslation
    # 10 x 10 grid of points on the bridge deck where to record responses.
    points = [
        Point(x=x, y=0, z=z)
        for x, z in itertools.product(
            np.linspace(c.bridge.x_min, c.bridge.x_max, 10),
            np.linspace(c.bridge.z_min, c.bridge.z_max, 10),
        )
    ]
    for damage_scenario in all_scenarios(c):
        response_array = responses_to_traffic_array(
            c=c,
            traffic_array=load_normal_traffic_array(c, mins=10)[0],
            response_type=response_type,
            bridge_scenario=damage_scenario,
            points=points,
            sim_runner=OSRunner,
        )
        print(response_array.shape)
        mean_response_array = np.mean(response_array, axis=0).T
        print(mean_response_array.shape)
        print(mean_response_array.shape)

        top_view_bridge(c.bridge, abutments=True, piers=True)
        responses = Responses.from_responses(
            response_type=response_type,
            responses=[(response_array[0][p], point) for p, point in enumerate(points)],
        )
        plot_contour_deck(c=c, responses=responses, center_norm=True, levels=100)
        plt.title(damage_scenario.name)
        plt.savefig(
            c.get_image_path("contour-mean-traffic-response", damage_scenario.name)
        )
        plt.close()


def point_load_response_plots(c: Config):
    """Response to normal traffic per damage scenario."""
    response_type = ResponseType.YTranslation
    # 10 x 10 grid of points on the bridge deck where to record responses.
    points = [
        Point(x=x, y=0, z=z)
        for x, z in itertools.product(
            np.linspace(c.bridge.x_min, c.bridge.x_max, 10),
            np.linspace(c.bridge.z_min, c.bridge.z_max, 10),
        )
    ]
    all_responses = []
    for damage_scenario in all_scenarios(c)[:3]:
        sim_params = SimParams(
            response_types=[response_type],
            ploads=[PointLoad(x_frac=0.5, z_frac=0.5, kn=1000)],
        )
        use_c = (
            damage_scenario.crack_config(c)
            if isinstance(damage_scenario, CrackedBridge)
            else c
        )
        print(use_c)
        all_responses.append(
            load_fem_responses(
                c=use_c,
                sim_params=sim_params,
                response_type=response_type,
                sim_runner=OSRunner(use_c),
                run=True,
            )
        )
    amin, amax = np.inf, -np.inf
    for sim_responses in all_responses:
        responses = np.array(list(sim_responses.values()))
        responses, _ = resize_units(responses, response_type)
        amin = min(amin, min(responses))
        amax = max(amax, max(responses))
        print(amin, amax)
    for d, damage_scenario in enumerate(all_scenarios(c)[:3]):
        top_view_bridge(c.bridge, abutments=True, piers=True)
        plot_contour_deck(
            c=c,
            responses=all_responses[d],
            levels=100,
            norm=colors.Normalize(vmin=amin, vmax=amax),
        )
        plt.title(damage_scenario.name)
        plt.savefig(
            c.get_image_path("contour-point-load-response", damage_scenario.name)
        )
        plt.close()


def cracked_concrete_plots(c: Config):
    """Contour plots of cracked concrete scenarios."""
    response_type = ResponseType.YTranslation
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
        traffic_array=load_normal_traffic_array(c)[0],
        response_type=response_type,
        bridge_scenario=cracked_scenario,
        points=points,
        sim_runner=OSRunner,
    )

    for t in range(len(response_array)):
        top_view_bridge(c.bridge, abutments=True, piers=True)
        responses = Responses.from_responses(
            response_type=response_type,
            responses=[(response_array[t][p], point) for p, point in enumerate(points)],
        )
        plot_contour_deck(c=c, responses=responses, center_norm=True)
        plt.title("Cracked Concrete")
        plt.savefig(c.get_image_path("cracked-scenario", f"cracked-time-{t}"))
        plt.close()


def each_pier_displacement_plots(c: Config):
    """Contour plots of pier displacement of each pier."""
    y = 0
    response_types = [ResponseType.YTranslation]

    for response_type in response_types:
        for p, pier in list(enumerate(c.bridge.supports)):
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
                pier_disp=equal_pier_disp(bridge=c.bridge, displacement=displacement),
                response_type=response_type,
                title=f"{response_type.name()} when each pier is displaced by {displacement} m",
            )

        # Gradient pier displacement scenario.
        for start, step in itertools.product([0.01, 0.02, 0.05], [0.01, 0.02, 0.05]):
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
    c: Config, pier_disp: PierDispBridge, response_type: ResponseType, title: str,
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
        traffic_array=np.zeros((1, len(c.bridge.wheel_tracks(c)) * c.il_num_loads)),
        response_type=response_type,
        bridge_scenario=pier_disp,
        points=points,
        fem_runner=OSRunner(c),
    )

    top_view_bridge(c.bridge, abutments=True, piers=True)
    responses = Responses.from_responses(
        response_type=response_type,
        responses=[(response_array[0][p], point) for p, point in enumerate(points)],
    )
    plot_contour_deck(c=c, responses=responses, center_norm=True)
    plt.title(title)
    plt.savefig(
        c.get_image_path("pier-scenarios", f"pier-displacement-{safe_str(title)}")
    )
    plt.close()


def comparison_plots_705(c: Config, run_only: bool):
    """Make contour plots for all verification points on bridge 705."""
    positions = [
        # (35, 25 - 16.6, None),
        (34.95459, 26.24579 - 16.6, "a"),
        (51.25051,     16.6 - 16.6, "b"),
        (89.98269, 9.445789 - 16.6, "c"),
        (102.5037, 6.954211 - 16.6, "d"),
        # (34.95459, 29.22606 - 16.6, "a"),
        # (51.25051, 16.6 - 16.6, "b"),
        # (92.40638, 12.405 - 16.6, "c"),
        # (101.7649, 3.973938 - 16.6, "d"),
    ]
    response_types = [ResponseType.YTranslation, ResponseType.Strain]
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
                sim_params=SimParams(ploads=loads, response_types=response_types),
            )
            if run_only:
                continue
            title = (
                f"{response_type.name()} from a {loads[0].kn} kN point load"
                + f"\nat x = {load_x:.3f}m, z = {load_z:.3f}m"
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
            plt.savefig(save(f"{label}-"))
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
            plt.savefig(save(f"{label}-center_norm-"))
            plt.close()

            # Finally create label/title the Diana plot.
            if label is not None:
                di_img = mpimg.imread(f"data/verification/diana-{label}.png")
                plt.imshow(di_img)
                plt.title(title)
                plt.xlabel("X position (mm)")
                plt.ylabel("Z position (mm)")
                plt.savefig(save(f"{label}-diana-"))
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
        for z in np.linspace(c.bridge.z_min, c.bridge.z_max, int(c.bridge.width)):
            pload = PointLoad(
                x_frac=c.bridge.x_frac(x), z_frac=c.bridge.z_frac(z), kn=100
            )
            fem_params = SimParams(ploads=[pload], response_types=[response_type])
            fem_responses = load_fem_responses(
                c=c,
                fem_params=fem_params,
                response_type=response_type,
                fem_runner=fem_runner,
            )
            X[-1].append(x)
            Z[-1].append(z)
            R[-1].append(fem_responses._at(x=x, y=0, z=z))

    cmap = get_cmap("bwr")
    plt.contourf(X, Z, R, levels=50, cmap=cmap)
    plt.show()
