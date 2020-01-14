"""Make contour plots."""
import itertools
from itertools import chain
from typing import List, Tuple

import matplotlib.colors as colors
import matplotlib.image as mpimg
import numpy as np
import pandas as pd
from matplotlib.cm import get_cmap

from classify.data.responses import responses_to_traffic_array
from classify.scenario.bridge import (
    CrackedBridge,
    HealthyBridge,
    PierDispBridge,
    equal_pier_disp,
    longitudinal_pier_disp,
)
from classify.scenarios import all_scenarios, cracked_scenario, unit_temp_scenario
from classify.vehicle import wagen1
from config import Config
from fem.params import SimParams
from fem.responses import Responses, load_fem_responses
from fem.run.opensees import OSRunner
from make.plot.distribution import load_normal_traffic_array
from model.bridge import Point
from model.load import DisplacementCtrl, PointLoad
from model.response import ResponseType
from plot import axis_colors, diana_cmap, diana_r_cmap, parula_cmap, plt
from plot.contour import contour_responses_3d
from plot.geometry import top_view_bridge
from plot.responses import plot_contour_deck, resize_and_units
from util import print_d, print_i, safe_str

# Print debug information for this file.
D: str = "make.plots.contour"
# D: bool = False


def cover_photo(c: Config, x: float, deformation_amp: float):
    """

    TODO: SimParams takes any loads iterable, to be flattened.
    TODO: Wrap SimRunner into Config.
    TODO: Ignore response type in SimParams (fill in by load_sim_responses).

    """
    response_type = ResponseType.YTranslation
    sim_responses = load_fem_responses(
        c=c,
        sim_runner=OSRunner(c),
        response_type=response_type,
        sim_params=SimParams(
            response_types=[response_type],
            ploads=list(
                chain.from_iterable(
                    wagen1.to_point_loads(
                        bridge=c.bridge, time=wagen1.time_at(x=x, bridge=c.bridge),
                    )
                )
            ),
        ),
    )
    shells = contour_responses_3d(c=c, sim_responses=sim_responses)
    for cmap in [
        parula_cmap,
        get_cmap("jet"),
        get_cmap("coolwarm"),
        get_cmap("viridis"),
    ]:
        contour_responses_3d(
            c=c,
            sim_responses=sim_responses,
            deformation_amp=deformation_amp,
            shells=shells,
            cmap=cmap,
        )
        plt.axis("off")
        plt.grid(False)
        plt.savefig(
            c.get_image_path(
                "cover-photo",
                f"cover-photo-deform-{deformation_amp}" f"-cmap-{cmap.name}.pdf",
            )
        )
        plt.close()


def traffic_response_plots(c: Config, times: int = 3):
    """Response to normal traffic per damage scenario at multiple time steps."""
    response_type = ResponseType.YTranslation
    # 10 x 10 grid of points on the bridge deck where to record responses.
    points = [
        Point(x=x, y=0, z=z)
        for x, z in itertools.product(
            np.linspace(c.bridge.x_min, c.bridge.x_max, 10),
            np.linspace(c.bridge.z_min, c.bridge.z_max, 10),
        )
    ]
    # for damage_scenario in all_scenarios(c):
    for damage_scenario in [unit_temp_scenario]:
        response_array = responses_to_traffic_array(
            c=c,
            traffic_array=load_normal_traffic_array(c, mins=1)[0],
            response_type=response_type,
            bridge_scenario=damage_scenario,
            points=points,
            sim_runner=OSRunner,
        )
        print(response_array.shape)
        mean_response_array = np.mean(response_array, axis=0).T
        print(mean_response_array.shape)
        print(mean_response_array.shape)

        for t in range(times):
            time_index = -1 + abs(t)
            top_view_bridge(c.bridge, abutments=True, piers=True)
            responses = Responses.from_responses(
                response_type=response_type,
                responses=[
                    (response_array[time_index][p], point)
                    for p, point in enumerate(points)
                ],
            )
            plot_contour_deck(c=c, responses=responses, center_norm=True, levels=100)
            plt.title(damage_scenario.name)
            plt.savefig(
                c.get_image_path(
                    "contour-traffic-response",
                    f"{damage_scenario.name}-time={time_index}",
                )
            )
            plt.close()


def point_load_response_plots(
    c: Config, x: float = 51.375, z: float = 0, kn: int = 1000
):
    """Response to a point load per damage scenario."""
    response_type = ResponseType.YTranslation
    # scenarios = all_scenarios(c)
    damage_scenarios = [HealthyBridge(), unit_temp_scenario]

    # 10 x 10 grid of points on the bridge deck where to record responses.
    points = [
        Point(x=x, y=0, z=z)
        for x, z in itertools.product(
            np.linspace(c.bridge.x_min, c.bridge.x_max, 10),
            np.linspace(c.bridge.z_min, c.bridge.z_max, 10),
        )
    ]
    all_responses = []
    for damage_scenario in damage_scenarios:
        sim_params = SimParams(
            response_types=[response_type],
            ploads=[
                PointLoad(x_frac=c.bridge.x_frac(x), z_frac=c.bridge.z_frac(z), kn=kn)
            ],
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
        responses, _ = resize_and_units(responses, response_type)
        amin = min(amin, min(responses))
        amax = max(amax, max(responses))
    for d, damage_scenario in enumerate(damage_scenarios):
        top_view_bridge(c.bridge, abutments=True, piers=True)
        plot_contour_deck(
            c=c,
            responses=all_responses[d],
            levels=100,
            norm=colors.Normalize(vmin=amin, vmax=amax),
        )
        plt.title(damage_scenario.name)
        plt.savefig(
            c.get_image_path(
                "contour-point-load-response",
                safe_str(f"{damage_scenario.name}-x-{x:.2f}-z-{z:.2f}-kn-{kn}"),
            )
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


def piers_displaced(c: Config):
    """Contour plots of pier displacement for the given pier indices."""
    pier_indices = [4, 5]
    color_bins = {
        4: [1.19,.8,.7,.6,.5,.4,.3,.2,.1,0,-.1,-.2,-.3,-.4,-.61],
        5: [1.36,1.05,.9,.75,.6,.45,.3,.15,0,-.15,-.3,-.45,-.6,-.75,-1.1],
    }
    y = 0
    response_types = [ResponseType.YTranslation, ResponseType.Strain]
    axis_values = pd.read_csv("validation/axis-screenshots/piers-min-max.csv")
    for r_i, response_type in enumerate(response_types):
        for p in pier_indices:
            # Construct unit string and get Axis values.
            if response_type == ResponseType.YTranslation:
                rt_str = "displa"
                unit_str = "mm"
            elif response_type == ResponseType.Strain:
                rt_str = "strain"
                unit_str = "MPa"
            else:
                raise ValueError("Unsupported response type")
            row = axis_values[axis_values["name"] == f"{p}-{rt_str}"]

            # Run the simulation and collect responses.
            pier = c.bridge.supports[p]
            pier_disp = DisplacementCtrl(displacement=c.pd_unit_disp, pier=p)
            sim_params = SimParams(
                response_types=response_types, displacement_ctrl=pier_disp,
            )
            sim_responses = load_fem_responses(
                c=c,
                sim_params=sim_params,
                response_type=response_type,
                sim_runner=OSRunner(c),
                run=r_i == 0,  # Only need to run it once.
            )

            # Map simulation strains to stresses.
            units = None
            if response_type == ResponseType.Strain:
                sim_responses.map(lambda v: v * c.bridge.sections[0].youngs * 1E-6)
                if len(c.bridge.sections) > 1:
                    raise ValueError("Expected only 1 deck section")
                units = "MPa"

            # Map simulation from 1m to 1mm.
            assert c.pd_unit_disp == 1
            sim_responses.map(lambda v: v / 1000)

            # Plot and save the image. If plotting strains use Axis values for
            # colour normalization.
            norm = None
            cmap = colors.LinearSegmentedColormap.from_list(
                "axis", list(reversed(axis_colors)), N=14)
            if response_type == ResponseType.Strain:
                bins = color_bins[p]
                assert len(bins) == 15
                norm = colors.BoundaryNorm(list(reversed(bins)), len(bins))
                plt.scatter(x=[0, 0], y=[0, 0], c=[bins[0], bins[-1]], alpha=0)
                sim_response_values = list(sim_responses.values())
            top_view_bridge(c.bridge, abutments=True, piers=True)
            plot_contour_deck(
                c=c,
                y=y,
                cmap=cmap,
                norm=norm,
                responses=sim_responses,
                levels=14,
                units=units,
                show_legend=response_type == ResponseType.YTranslation,
            )
            plt.title(f"{response_type.name()} from pier settlement of 1 mm")
            plt.savefig(
                c.get_image_path(
                    "validation/pier-displacement",
                    safe_str(f"pier-{p}-{response_type.name()}") + ".pdf",
                )
            )
            plt.close()

            # Save the axis plots.
            axis_img = mpimg.imread(
                f"validation/axis-screenshots/{p}-{rt_str}.png"
            )
            top_view_bridge(c.bridge, abutments=True)
            plt.imshow(
                axis_img,
                extent=(
                    c.bridge.x_min,
                    c.bridge.x_max,
                    c.bridge.z_min,
                    c.bridge.z_max,
                ),
            )
            # Plot the load and min, max values.
            amin, amax = float(row["min"]), float(row["max"])
            for point, leg_label, color in [
                ((0, 0), f"min = {np.around(amin, 3)} {unit_str}", "r"),
                ((0, 0), f"max = {np.around(amax, 3)} {unit_str}", "r"),
                ((0, 0), f"|min-max| = {np.around(abs(amax - amin), 3)} {unit_str}", "r"),
            ]:
                plt.scatter(
                    [point[0]],
                    [point[1]],
                    label=leg_label,
                    marker="o",
                    color=color,
                    alpha=0,
                )
            if response_type == ResponseType.YTranslation:
                plt.legend()
            # Add the Axis colorbar.
            plt.imshow(np.array([[amin, amax]]), cmap=cmap, norm=norm, extent=(0, 0, 0, 0))
            clb = plt.colorbar()
            clb.ax.set_title(unit_str)
            # Title and save.
            plt.title(f"{response_type.name()} from pier settlement of 1 mm")
            plt.xlabel("X position (m)")
            plt.ylabel("Z position (m)")
            plt.savefig(c.get_image_path(
                "validation/pier-displacement",
                f"{p}-axis-{rt_str}",
            ))
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
        (34.95459, 26.24579 - 16.6, "a"),
        (51.25051, 16.6 - 16.6, "b"),
        (89.98269, 9.445789 - 16.6, "c"),
        (102.5037, 6.954211 - 16.6, "d"),
        # (34.95459, 29.22606 - 16.6, "a"),
        # (51.25051, 16.6 - 16.6, "b"),
        # (92.40638, 12.405 - 16.6, "c"),
        # (101.7649, 3.973938 - 16.6, "d"),
    ]
    diana_values = pd.read_csv("validation/diana-screenshots/min-max.csv")
    response_types = [ResponseType.YTranslation, ResponseType.Strain]
    # For each response type and loading position first create contour plots for
    # OpenSees. Then finally create subplots comparing to Diana.
    for response_type in response_types:
        cmap = diana_cmap if response_type == ResponseType.Strain else diana_r_cmap
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
                "validation/diana-comp",
                safe_str(f"{prefix}{response_type.name()}") + ".pdf",
            )
            top_view_bridge(c.bridge, piers=True, abutments=True)
            plot_contour_deck(c=c, responses=fem_responses, ploads=loads, cmap=cmap)
            plt.title(title)
            plt.tight_layout()
            plt.savefig(save(f"{label}-"))
            plt.close()

            # Finally create label/title the Diana plot.
            if label is not None:
                if response_type == ResponseType.YTranslation:
                    rt_str = "displa"
                    unit_str = "mm"
                elif response_type == ResponseType.Strain:
                    rt_str = "strain"
                    unit_str = "m/m"
                else:
                    raise ValueError("Unsupported response type")
                di_img = mpimg.imread(
                    f"validation/diana-screenshots/{label}-{rt_str}.png"
                )
                top_view_bridge(c.bridge, piers=True, abutments=True)
                plt.imshow(
                    di_img,
                    extent=(
                        c.bridge.x_min,
                        c.bridge.x_max,
                        c.bridge.z_min,
                        c.bridge.z_max,
                    ),
                )

                # Plot the load and min, max values.
                row = diana_values[diana_values["name"] == f"{label}-{rt_str}"]
                amin, amax = float(row["min"]), float(row["max"])
                if response_type == ResponseType.Strain:
                    amax, amin = -amin * 1e6, -amax * 1e6
                    # amax, amin = amax * 1e6, amin * 1e6
                for point, leg_label, color, alpha in [
                    ((load_x, load_z), f"{loads[0].kn} kN load", "r", 1),
                    ((0, 0), f"min = {amin:.2f} {unit_str}", "r", 0),
                    ((0, 0), f"max = {amax:.2f} {unit_str}", "r", 0),
                    ((0, 0), f"|min-max| = {abs(amax - amin):.2f} {unit_str}", "r", 0),
                ]:
                    plt.scatter(
                        [point[0]],
                        [point[1]],
                        label=leg_label,
                        marker="o",
                        color=color,
                        alpha=alpha,
                    )
                plt.legend()

                # Add the Diana colorbar.
                plt.imshow(np.array([[amin, amax]]), cmap=cmap, extent=(0, 0, 0, 0))
                clb = plt.colorbar()
                clb.ax.set_title(unit_str)

                plt.title(title)
                plt.xlabel("X position (m)")
                plt.ylabel("Z position (m)")
                plt.tight_layout()
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
